from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.db import models as fields
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists
from opal import models
from entrytool.models import Hospital


class MMRegimenList(lookuplists.LookupList):
    class Meta:
        verbose_name = _("MM Regimen List")
        verbose_name_plural = _("MM Regimen List")


class MMStopReason(lookuplists.LookupList):
    class Meta:
        verbose_name = _("MM Stop Reason List")
        verbose_name_plural = _("MM Stop Reason List")


class MMDiagnosisDetails(models.EpisodeSubrecord):
    _is_singleton = True  # One entry per patient that is updated

    CHOICES = (("Yes", _("Yes")), ("No", _("No")), ("Unknown", _("Unknown")))

    HEAVY_CHAIN_OPTIONS = (
        ("IgG", _("IgG"),),
        ("IgD", _("IgD"),),
        ("IgA", _("IgA"),),
        ("IgM", _("IgM"),),
        ("IgE", _("IgE"),),
        ("No Heavy Chain", _("No Heavy Chain"),),
        ("Other", _("Other"),),
    )

    LIGHT_CHAIN_OPTIONS = (
        ('Kappa', _('Kappa')),
        ('Lambda', _('Lambda')),
        ('Non-Secretory', _('Non-Secretory')),
        ('No Light Chain', _('No Light Chain'))
    )

    ISS_STAGES = (
        ("Stage I", _("Stage I")),
        ("Stage II", _("Stage II")),
        ("Stage III", _("Stage III")),
        ("Unknown", _("Unknown")),
    )
    R_ISS_STAGES = (
        ('I', _("I")),
        ('II', _("II")),
        ('III', _("III")),
    )
    PP_TYPE_CHOICES = (
        ("IgG", _("IgG")),
        ("IgA", _("IgA")),
        ("IgE", _("IgE")),
        ("Light Chain Myeloma", _("Light Chain Myeloma")),
    )
    hospital = models.ForeignKeyOrFreeText(Hospital, verbose_name=_("Hospital"))
    diag_date = fields.DateField(
        blank=False, null=True, verbose_name=_("Date of Diagnosis")
    )
    heavy_chain_type = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=HEAVY_CHAIN_OPTIONS,
        verbose_name=_("Heavy chain type")
    )
    light_chain_type = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=LIGHT_CHAIN_OPTIONS,
        verbose_name=_("Light chain type")
    )
    smm_history = fields.CharField(
        blank=True, null=True,max_length=10, choices=CHOICES, verbose_name=_("History of SMM")
    )
    smm_history_date = fields.DateField(
        blank=True, null=True, verbose_name=_("Date of SMM diagnosis")
    )
    mgus_history = fields.CharField(
        blank=True, null=True, max_length=10, choices=CHOICES, verbose_name=_("History of MGUS")
    )
    mgus_history_date = fields.DateField(
        blank=True, null=True, verbose_name=_("Date of MGUS Diagnosis")
    )
    iss_stage = fields.CharField(
        blank=True, null=True, max_length=10, choices=ISS_STAGES, verbose_name=_("ISS Stage")
    )
    r_iss_stage = fields.CharField(
        blank=True, null=True, max_length=10, choices=R_ISS_STAGES, verbose_name=_("R ISS Stage")
    )
    ds_stage = fields.CharField(
        blank=True, null=True, max_length=10, choices=ISS_STAGES, verbose_name=_("DS Stage")
    )
    pp_type = fields.CharField(
        blank=True, null=True, max_length=50, choices=PP_TYPE_CHOICES, verbose_name=_("PP Type")
    )
    del_17p = fields.CharField(
        blank=True, null=True, max_length=10, choices=CHOICES, verbose_name=_("del(17)p")
    )
    del_13 = fields.CharField(blank=True, null=True, max_length=10, choices=CHOICES, verbose_name=_("del13"))
    t4_14 = fields.CharField(blank=True, null=True, max_length=10, choices=CHOICES, verbose_name=_("t(4;14)"))
    t4_16 = fields.CharField(blank=True, null=True, max_length=10, choices=CHOICES, verbose_name=_("t(4;16)"))

    class Meta:
        verbose_name = _("Diagnosis Details")
        verbose_name_plural = _("Diagnosis Details")


class MMRegimen(models.EpisodeSubrecord):
    _sort = "start_date"
    order_by = "-start_date"

    REGIMEN_TYPES = (
        ("Induction", _("Induction")),
        ("Maintenance", _("Maintenance")),
        ("Conditioning", _("Conditioning")),
        ("Watch and wait", _("Watch and wait")),
    )

    hospital = models.ForeignKeyOrFreeText(Hospital, verbose_name=_("Hospital"))
    nbCycles = fields.IntegerField(
        verbose_name=_("Number of Cycles"),
        null=True,
        blank=True,
    )
    start_date = fields.DateField(
        verbose_name=_("Start Date"), blank=True, null=True
    )
    end_date = fields.DateField(verbose_name=_("End Date"), blank=True, null=True)
    regimen = ForeignKeyOrFreeText(MMRegimenList, verbose_name=_("Regimen"))
    radiotherapy = fields.BooleanField(
        default=False, verbose_name=_("Radiotherapy")
    )
    category = fields.CharField(
        max_length=40, choices=REGIMEN_TYPES, verbose_name=_("Regimen Type")
    )
    stop_reason = ForeignKeyOrFreeText(
        MMStopReason, verbose_name=_("Reason for Regimen Stop")
    )
    end_treatment_reason = fields.TextField(
        blank=True, default="", verbose_name=_("End Treatment Reason")
    )

    class Meta:
        verbose_name = _("Regimen")
        verbose_name_plural = _("Regimens")


class MMResponse(models.EpisodeSubrecord):
    _sort = "response_date"
    order_by = "-response_date"
    RESPONSES = (
        ("Minimal response", _("Minimal response")),
        ("Partial response", _("Partial response")),
        ("Very good partial response", _("Very good partial response")),
        ("Complete response", _("Complete response")),
        ("Stringent complete response", _("Stringent complete response")),
        ("Near complete response", _("Near complete response")),
        ("Immunophenotypic complete response", _("Immunophenotypic complete response")),
        ("Stable disease", _("Stable disease")),
        ("Progressive disease", _("Progressive disease")),
        ("Response unknown/NA", _("Response unknown/NA")),
    )
    progression_date = fields.DateField(
        blank=True, null=True, verbose_name=_("Progression Date")
    )
    response_date = fields.DateField(verbose_name=_("Response Date"))
    response = fields.CharField(
        blank=True,
        null=True,
        max_length=50,
        choices=RESPONSES,
        verbose_name=_("Response")
    )

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")


class MMStemCellTransplantEligibility(models.EpisodeSubrecord):
    _is_singleton = True
    eligible_for_stem_cell_transplant = fields.BooleanField(
        default=False, verbose_name=_("Eligible For Stem Cell Transplant")
    )

    class Meta:
        verbose_name = _("Stem Cell Transplant Eligibility")
        verbose_name_plural = _("Stem Cell Transplant Eligibilities")


def delete_stem_cells(sender, instance, **kwargs):
    instance.episode.sct_set.all().delete()


post_save.connect(
    delete_stem_cells, sender=MMStemCellTransplantEligibility
)


class LabTest(models.EpisodeSubrecord):
    _sort = "date"
    _icon = "fa fa-stethoscope"

    class Meta:
        verbose_name = _("Lab Tests")
        verbose_name_plural = _("Lab Tests")

    HEAVY_CHAIN_OPTIONS = (
        ("IgG", _("IgG"),),
        ("IgD", _("IgD"),),
        ("IgA", _("IgA"),),
        ("IgM", _("IgM"),),
        ("IgE", _("IgE"),),
        ("No Heavy Chain", _("No Heavy Chain"),),
        ("Other", _("Other"),),
    )

    LIGHT_CHAIN_OPTIONS = (
        ('Kappa', _('Kappa')),
        ('Lambda', _('Lambda')),
        ('Non-Secretory', _('Non-Secretory')),
        ('No Light Chain', _('No Light Chain'))
    )

    hospital = models.ForeignKeyOrFreeText(Hospital, verbose_name=_("Hospital"))
    date = fields.DateField(verbose_name=_("Date"), blank=True, null=True)

    LDH = fields.FloatField(blank=True, null=True, verbose_name=_("LDH"))
    beta2m = fields.FloatField(blank=True, null=True, verbose_name=_("beta2m"))
    albumin = fields.FloatField(blank=True, null=True, verbose_name=_("Albumin"))
    # mg/dL, min 0.5, max 20
    creatinine = fields.FloatField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Creatinine Clearance")
    )

    # mg/dL, min 6.5, max 25
    calcium = fields.FloatField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Calcium")
    )
    mprotein_urine = fields.FloatField(blank=True, null=True, verbose_name=_("MProtein Urine"))
    mprotein_serum = fields.FloatField(blank=True, null=True ,verbose_name=("MProtein Serum"))
    mprotein_24h = fields.FloatField(blank=True, null=True, verbose_name=_("Mprotein in 24 hour"))

    igg_count = fields.FloatField(blank=True, null=True, verbose_name="IgG Count")
    igd_count = fields.FloatField(blank=True, null=True, verbose_name="IgD Count")
    iga_count = fields.FloatField(blank=True, null=True, verbose_name="IgA Count")
    igm_count = fields.FloatField(blank=True, null=True, verbose_name="IgM Count")
    ige_count = fields.FloatField(blank=True, null=True, verbose_name="IgE Count")

    heavy_chain_type = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=HEAVY_CHAIN_OPTIONS,
        verbose_name=_("Heavy Chain Type")
    )
    # I don't think we need this but...
    heavy_chain_type_other = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Heavy Chain Type Other")
    )
    light_chain_type = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=LIGHT_CHAIN_OPTIONS,
        verbose_name=_("Light Chain Type")
    )

    lambda_light_chain_count = fields.FloatField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Lambda Count")
    )
    kappa_light_chain_count = fields.FloatField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Kappa Count")
    )
    kappa_lambda_ratio = fields.FloatField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name=_("Kappa Lambda Ratio")
    )


class MMCytogenetics(models.EpisodeSubrecord):
    class Meta:
        verbose_name = _("Cytogenetics")
        verbose_name_plural = _("Cytogenetics")

    CHOICES = (
        ("Positive", _("Positive")),
        ("Negative", _("Negative")),
        ("Unknown", _("Unknown")),
    )

    CHOICES_IGHV = (
        ("Mutated", _("Mutated")),
        ("Non-mutated", _("Non-mutated")),
        ("Unknown", _("Unknown")),
    )

    hospital = models.ForeignKeyOrFreeText(Hospital, verbose_name=_("Hospital"))
    date = fields.DateField(blank=True, null=True, verbose_name=_("Date"))

    tp_53 = fields.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=CHOICES,
        verbose_name=_("tp 53")
    )
    t4_14 = fields.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=CHOICES,
        verbose_name=_("t4;14")
    )
    t4_14_haploid_karyotype = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name=_("t(4;14) Haploid Karyotype")
    )
    t4_14_16 = fields.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=CHOICES,
        verbose_name=_("t14;16")
    )
    t4_14_not_effected = fields.CharField(
        blank=True,
        null=True,
        max_length=256,
        choices=CHOICES,
        verbose_name=_("t(4;14) Not Effected")
    )
    t11_14 = fields.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=CHOICES,
        verbose_name=_("t(11;14)")
    )
    del1p = fields.CharField(
        max_length=10, choices=CHOICES, verbose_name=_("del 1p")
    )

    amp1q21 = fields.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=CHOICES,
        verbose_name=_("amp 1q21")
    )

    del_17p = fields.CharField(
        max_length=10, choices=CHOICES, verbose_name=_("del 17p")
    )

    ighv = fields.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=CHOICES,
        verbose_name=_("IGHV"),
    )
