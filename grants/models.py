from django.db import models
from urlman import Urls


class Program(models.Model):
    """
    Something which is giving out grants - a workshop, a course,
    a conference, etc.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    applications_open = models.DateTimeField(blank=True, null=True)
    applications_close = models.DateTimeField(blank=True, null=True)
    grants_announced = models.DateTimeField(blank=True, null=True)
    program_starts = models.DateTimeField(blank=True, null=True)

    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class urls(Urls):
        view = "/{self.slug}/"
        questions = "{view}questions/"
        applicants = "{view}applicants/"
        applicants_bulk = "{view}applicants/bulk/"
        scores_bulk = "{view}applicants/bulk_scores/"
        resources = "{view}resources/"
        users = "{view}users/"
        admin = "{view}admin/"
        apply = "{view}apply/"
        apply_success = "{view}apply/success/"


class Resource(models.Model):
    """
    A resource that can be given out to grantees, be it a place, some
    money, free tickets, or so on. Always countable as integers.
    """

    TYPE_CHOICES = [
        ("money", "Money"),
        ("ticket", "Ticket"),
        ("place", "Place"),
        ("accomodation", "Accomodation"),
    ]

    program = models.ForeignKey(Program, related_name="resources")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    amount = models.PositiveIntegerField()

    class urls(Urls):
        edit = "{self.program.urls.resources}{self.id}/"


class Question(models.Model):
    """
    A question asked of applicants.
    """

    TYPE_CHOICES = [
        ("boolean", "Yes/No"),
        ("text", "Short text"),
        ("textarea", "Long text"),
        ("integer", "Integer value"),
    ]

    program = models.ForeignKey(Program, related_name="questions")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    question = models.TextField()
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class urls(Urls):
        edit = "{self.program.urls.questions}{self.id}/"

    def can_delete(self):
        return not self.answers.exists()


class Applicant(models.Model):
    """
    Someone applying for a grant.
    """

    program = models.ForeignKey(Program, related_name="applicants")
    name = models.TextField()
    email = models.EmailField()

    applied = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = [
            ("program", "email"),
        ]

    class urls(Urls):
        view = "{self.program.urls.applicants}{self.id}/"

    def __unicode__(self):
        return self.name

    def average_score(self):
        scores = [s.score for s in self.scores.all() if s.score]
        if not scores:
            return None
        else:
            return sum(scores) / float(len(scores))


class Answer(models.Model):
    """
    An applicant's answer to a question.
    """

    applicant = models.ForeignKey(Applicant, related_name="answers")
    question = models.ForeignKey(Question, related_name="answers")
    answer = models.TextField()

    class Meta:
        unique_together = [
            ("applicant", "question"),
        ]


class Score(models.Model):
    """
    A score and optional comment on an applicant by a user.
    """

    applicant = models.ForeignKey(Applicant, related_name="scores")
    user = models.ForeignKey("users.User", related_name="scores")
    score = models.FloatField(blank=True, null=True, help_text="From 0 (terrible) to 5 (excellent)")
    comment = models.TextField(blank=True, null=True, help_text="Seen only by other voters, not by the applicant")
    score_history = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [
            ("applicant", "user"),
        ]

    def score_history_human(self):
        return (self.score_history or "").replace(",", ", ")
