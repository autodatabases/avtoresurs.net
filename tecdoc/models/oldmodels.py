# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AliCoordinates(models.Model):
    aco_gra_id = models.CharField(db_column='ACO_GRA_ID', max_length=11)  # Field name made lowercase.
    aco_gra_lng_id = models.SmallIntegerField(db_column='ACO_GRA_LNG_ID')  # Field name made lowercase.
    aco_ali_art_id = models.IntegerField(db_column='ACO_ALI_ART_ID')  # Field name made lowercase.
    aco_ali_sort = models.SmallIntegerField(db_column='ACO_ALI_SORT')  # Field name made lowercase.
    aco_sort = models.SmallIntegerField(db_column='ACO_SORT')  # Field name made lowercase.
    aco_type = models.SmallIntegerField(db_column='ACO_TYPE', blank=True, null=True)  # Field name made lowercase.
    aco_x1 = models.SmallIntegerField(db_column='ACO_X1', blank=True, null=True)  # Field name made lowercase.
    aco_y1 = models.SmallIntegerField(db_column='ACO_Y1', blank=True, null=True)  # Field name made lowercase.
    aco_x2 = models.SmallIntegerField(db_column='ACO_X2', blank=True, null=True)  # Field name made lowercase.
    aco_y2 = models.SmallIntegerField(db_column='ACO_Y2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ali_coordinates'


class ArtCountrySpecifics(models.Model):
    acs_art_id = models.IntegerField(db_column='ACS_ART_ID')  # Field name made lowercase.
    acs_pack_unit = models.IntegerField(db_column='ACS_PACK_UNIT', blank=True, null=True)  # Field name made lowercase.
    acs_quantity_per_unit = models.IntegerField(db_column='ACS_QUANTITY_PER_UNIT', blank=True,
                                                null=True)  # Field name made lowercase.
    acs_kv_status_des_id = models.IntegerField(db_column='ACS_KV_STATUS_DES_ID', blank=True,
                                               null=True)  # Field name made lowercase.
    acs_kv_status = models.CharField(db_column='ACS_KV_STATUS', max_length=9, blank=True,
                                     null=True)  # Field name made lowercase.
    acs_status_date = models.DateTimeField(db_column='ACS_STATUS_DATE', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'art_country_specifics'


class ArtLookup(models.Model):
    arl_art_id = models.IntegerField(primary_key=True, db_column='ARL_ART_ID')  # Field name made lowercase.
    arl_search_number = models.CharField(db_column='ARL_SEARCH_NUMBER', max_length=105, blank=True,
                                         null=True)  # Field name made lowercase.
    arl_kind = models.CharField(db_column='ARL_KIND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    arl_bra_id = models.SmallIntegerField(db_column='ARL_BRA_ID', blank=True, null=True)  # Field name made lowercase.
    arl_display_nr = models.CharField(db_column='ARL_DISPLAY_NR', max_length=105, blank=True,
                                      null=True)  # Field name made lowercase.
    arl_display = models.SmallIntegerField(db_column='ARL_DISPLAY', blank=True, null=True)  # Field name made lowercase.
    arl_block = models.SmallIntegerField(db_column='ARL_BLOCK', blank=True, null=True)  # Field name made lowercase.
    arl_sort = models.SmallIntegerField(db_column='ARL_SORT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'art_lookup'


class ArticleListCriteria(models.Model):
    alc_ali_art_id = models.IntegerField(db_column='ALC_ALI_ART_ID')  # Field name made lowercase.
    alc_ali_sort = models.SmallIntegerField(db_column='ALC_ALI_SORT')  # Field name made lowercase.
    alc_sort = models.SmallIntegerField(db_column='ALC_SORT', blank=True, null=True)  # Field name made lowercase.
    alc_cri_id = models.SmallIntegerField(db_column='ALC_CRI_ID', blank=True, null=True)  # Field name made lowercase.
    alc_value = models.CharField(db_column='ALC_VALUE', max_length=60, blank=True,
                                 null=True)  # Field name made lowercase.
    alc_kv_des_id = models.IntegerField(db_column='ALC_KV_DES_ID', blank=True, null=True)  # Field name made lowercase.
    alc_typ_id = models.IntegerField(db_column='ALC_TYP_ID', blank=True, null=True)  # Field name made lowercase.
    alc_eng_id = models.IntegerField(db_column='ALC_ENG_ID', blank=True, null=True)  # Field name made lowercase.
    alc_axl_id = models.IntegerField(db_column='ALC_AXL_ID', blank=True, null=True)  # Field name made lowercase.
    alc_mrk_id = models.IntegerField(db_column='ALC_MRK_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article_list_criteria'


class Articles(models.Model):
    art_id = models.IntegerField(primary_key=True, db_column='ART_ID')  # Field name made lowercase.
    art_article_nr = models.CharField(db_column='ART_ARTICLE_NR', max_length=66)  # Field name made lowercase.
    art_sup_id = models.SmallIntegerField(db_column='ART_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    art_des_id = models.IntegerField(db_column='ART_DES_ID', blank=True, null=True)  # Field name made lowercase.
    art_complete_des_id = models.IntegerField(db_column='ART_COMPLETE_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    art_pack_selfservice = models.SmallIntegerField(db_column='ART_PACK_SELFSERVICE', blank=True,
                                                    null=True)  # Field name made lowercase.
    art_material_mark = models.SmallIntegerField(db_column='ART_MATERIAL_MARK', blank=True,
                                                 null=True)  # Field name made lowercase.
    art_replacement = models.SmallIntegerField(db_column='ART_REPLACEMENT', blank=True,
                                               null=True)  # Field name made lowercase.
    art_accessory = models.SmallIntegerField(db_column='ART_ACCESSORY', blank=True,
                                             null=True)  # Field name made lowercase.
    art_batch_size1 = models.IntegerField(db_column='ART_BATCH_SIZE1', blank=True,
                                          null=True)  # Field name made lowercase.
    art_batch_size2 = models.IntegerField(db_column='ART_BATCH_SIZE2', blank=True,
                                          null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'articles'


class ArticlesNew(models.Model):
    artn_sup_id = models.SmallIntegerField(db_column='ARTN_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    artn_art_id = models.IntegerField(db_column='ARTN_ART_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'articles_new'


class Brands(models.Model):
    bra_id = models.SmallIntegerField(db_column='BRA_ID')  # Field name made lowercase.
    bra_mfc_code = models.CharField(db_column='BRA_MFC_CODE', max_length=60, blank=True,
                                    null=True)  # Field name made lowercase.
    bra_brand = models.CharField(db_column='BRA_BRAND', max_length=60, blank=True,
                                 null=True)  # Field name made lowercase.
    bra_mf_nr = models.IntegerField(db_column='BRA_MF_NR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'brands'


class Countries(models.Model):
    cou_id = models.SmallIntegerField(db_column='COU_ID')  # Field name made lowercase.
    cou_cc = models.CharField(db_column='COU_CC', max_length=9, blank=True, null=True)  # Field name made lowercase.
    cou_des_id = models.IntegerField(db_column='COU_DES_ID', blank=True, null=True)  # Field name made lowercase.
    cou_currency_code = models.CharField(db_column='COU_CURRENCY_CODE', max_length=9, blank=True,
                                         null=True)  # Field name made lowercase.
    cou_iso2 = models.CharField(db_column='COU_ISO2', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cou_is_group = models.SmallIntegerField(db_column='COU_IS_GROUP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'countries'


class Criteria(models.Model):
    cri_id = models.SmallIntegerField(db_column='CRI_ID')  # Field name made lowercase.
    cri_des_id = models.IntegerField(db_column='CRI_DES_ID')  # Field name made lowercase.
    cri_short_des_id = models.IntegerField(db_column='CRI_SHORT_DES_ID', blank=True,
                                           null=True)  # Field name made lowercase.
    cri_unit_des_id = models.IntegerField(db_column='CRI_UNIT_DES_ID', blank=True,
                                          null=True)  # Field name made lowercase.
    cri_type = models.CharField(db_column='CRI_TYPE', max_length=1)  # Field name made lowercase.
    cri_kt_id = models.SmallIntegerField(db_column='CRI_KT_ID', blank=True, null=True)  # Field name made lowercase.
    cri_is_interval = models.SmallIntegerField(db_column='CRI_IS_INTERVAL', blank=True,
                                               null=True)  # Field name made lowercase.
    cri_successor = models.SmallIntegerField(db_column='CRI_SUCCESSOR', blank=True,
                                             null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'criteria'


class DesTexts(models.Model):
    tex_id = models.IntegerField(primary_key=True, db_column='TEX_ID')  # Field name made lowercase.
    tex_text = models.CharField(db_column='TEX_TEXT', max_length=1200, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'des_texts'


class CountryDesignations(models.Model):
    cds_id = models.IntegerField(primary_key=True, db_column='CDS_ID')  # Field name made lowercase.
    cds_lng_id = models.SmallIntegerField(db_column='CDS_LNG_ID')  # Field name made lowercase.
    cds_tex_id = models.ForeignKey(DesTexts, db_column='CDS_TEX_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'country_designations'


class Designations(models.Model):
    des_id = models.IntegerField(primary_key=True, db_column='DES_ID')  # Field name made lowercase.
    des_lng_id = models.SmallIntegerField(db_column='DES_LNG_ID')  # Field name made lowercase.
    des_tex_id = models.IntegerField(db_column='DES_TEX_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'designations'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class LaCriteria(models.Model):
    lac_la_id = models.IntegerField(db_column='LAC_LA_ID')  # Field name made lowercase.
    lac_sort = models.IntegerField(db_column='LAC_SORT')  # Field name made lowercase.
    lac_cri_id = models.SmallIntegerField(db_column='LAC_CRI_ID')  # Field name made lowercase.
    lac_value = models.CharField(db_column='LAC_VALUE', max_length=60, blank=True,
                                 null=True)  # Field name made lowercase.
    lac_kv_des_id = models.IntegerField(db_column='LAC_KV_DES_ID', blank=True, null=True)  # Field name made lowercase.
    lac_display = models.SmallIntegerField(db_column='LAC_DISPLAY', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'la_criteria'


class LaInfo(models.Model):
    lin_la_id = models.IntegerField(db_column='LIN_LA_ID')  # Field name made lowercase.
    lin_sort = models.SmallIntegerField(db_column='LIN_SORT')  # Field name made lowercase.
    lin_kv_type = models.CharField(db_column='LIN_KV_TYPE', max_length=9)  # Field name made lowercase.
    lin_display = models.SmallIntegerField(db_column='LIN_DISPLAY')  # Field name made lowercase.
    lin_tmo_id = models.IntegerField(db_column='LIN_TMO_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'la_info'


class Languages(models.Model):
    lng_id = models.SmallIntegerField(db_column='LNG_ID')  # Field name made lowercase.
    lng_des_id = models.IntegerField(db_column='LNG_DES_ID', blank=True, null=True)  # Field name made lowercase.
    lng_iso2 = models.CharField(db_column='LNG_ISO2', max_length=6, blank=True, null=True)  # Field name made lowercase.
    lng_codepage = models.CharField(db_column='LNG_CODEPAGE', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'languages'


class LinkArt(models.Model):
    la_id = models.IntegerField(db_column='LA_ID')  # Field name made lowercase.
    la_art_id = models.IntegerField(db_column='LA_ART_ID')  # Field name made lowercase.
    la_ga_id = models.IntegerField(db_column='LA_GA_ID')  # Field name made lowercase.
    la_sort = models.IntegerField(db_column='LA_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_art'


class LinkArtGa(models.Model):
    lag_art_id = models.IntegerField(db_column='LAG_ART_ID')  # Field name made lowercase.
    lag_ga_id = models.IntegerField(db_column='LAG_GA_ID')  # Field name made lowercase.
    lag_sup_id = models.SmallIntegerField(db_column='LAG_SUP_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_art_ga'


class LinkCabTyp(models.Model):
    lct_typ_id = models.IntegerField(db_column='LCT_TYP_ID')  # Field name made lowercase.
    lct_nr = models.SmallIntegerField(db_column='LCT_NR')  # Field name made lowercase.
    lct_cab_id = models.IntegerField(db_column='LCT_CAB_ID')  # Field name made lowercase.
    lct_pcon_start = models.IntegerField(db_column='LCT_PCON_START', blank=True,
                                         null=True)  # Field name made lowercase.
    lct_pcon_end = models.IntegerField(db_column='LCT_PCON_END', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_cab_typ'


class LinkGaCri(models.Model):
    lgc_ga_nr = models.SmallIntegerField(db_column='LGC_GA_NR')  # Field name made lowercase.
    lgc_cri_id = models.SmallIntegerField(db_column='LGC_CRI_ID')  # Field name made lowercase.
    lgc_sort = models.SmallIntegerField(db_column='LGC_SORT')  # Field name made lowercase.
    lgc_suggestion = models.IntegerField(db_column='LGC_SUGGESTION')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_ga_cri'


class LinkGaStr(models.Model):
    lgs_str_id = models.IntegerField(primary_key=True, db_column='LGS_STR_ID')  # Field name made lowercase.
    lgs_ga_id = models.IntegerField(db_column='LGS_GA_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_ga_str'


class LinkGraArt(models.Model):
    lga_art_id = models.IntegerField(db_column='LGA_ART_ID')  # Field name made lowercase.
    lga_sort = models.SmallIntegerField(db_column='LGA_SORT')  # Field name made lowercase.
    lga_gra_id = models.CharField(db_column='LGA_GRA_ID', max_length=11)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_gra_art'


class LinkGraLa(models.Model):
    lgl_la_id = models.IntegerField(db_column='LGL_LA_ID')  # Field name made lowercase.
    lgl_typ_id = models.IntegerField(db_column='LGL_TYP_ID', blank=True, null=True)  # Field name made lowercase.
    lgl_eng_id = models.IntegerField(db_column='LGL_ENG_ID', blank=True, null=True)  # Field name made lowercase.
    lgl_axl_id = models.IntegerField(db_column='LGL_AXL_ID', blank=True, null=True)  # Field name made lowercase.
    lgl_mrk_id = models.IntegerField(db_column='LGL_MRK_ID', blank=True, null=True)  # Field name made lowercase.
    lgl_sort = models.SmallIntegerField(db_column='LGL_SORT')  # Field name made lowercase.
    lgl_gra_id = models.CharField(db_column='LGL_GRA_ID', max_length=11)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_gra_la'


class LinkLaAxl(models.Model):
    laa_la_id = models.IntegerField(db_column='LAA_LA_ID')  # Field name made lowercase.
    laa_axl_id = models.IntegerField(db_column='LAA_AXL_ID')  # Field name made lowercase.
    laa_ga_id = models.IntegerField(db_column='LAA_GA_ID')  # Field name made lowercase.
    laa_sup_id = models.SmallIntegerField(db_column='LAA_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    laa_sort = models.IntegerField(db_column='LAA_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_axl'


class LinkLaAxlNew(models.Model):
    laan_la_id = models.IntegerField(db_column='LAAN_LA_ID')  # Field name made lowercase.
    laan_axl_id = models.IntegerField(db_column='LAAN_AXL_ID')  # Field name made lowercase.
    laan_ga_id = models.IntegerField(db_column='LAAN_GA_ID')  # Field name made lowercase.
    laan_sup_id = models.SmallIntegerField(db_column='LAAN_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    laan_sort = models.IntegerField(db_column='LAAN_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_axl_new'


class LinkLaEng(models.Model):
    lae_la_id = models.IntegerField(db_column='LAE_LA_ID')  # Field name made lowercase.
    lae_eng_id = models.IntegerField(db_column='LAE_ENG_ID')  # Field name made lowercase.
    lae_ga_id = models.IntegerField(db_column='LAE_GA_ID')  # Field name made lowercase.
    lae_sup_id = models.SmallIntegerField(db_column='LAE_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    lae_sort = models.IntegerField(db_column='LAE_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_eng'


class LinkLaEngNew(models.Model):
    laen_sup_id = models.SmallIntegerField(db_column='LAEN_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    laen_ga_id = models.IntegerField(db_column='LAEN_GA_ID')  # Field name made lowercase.
    laen_la_id = models.IntegerField(db_column='LAEN_LA_ID')  # Field name made lowercase.
    laen_eng_id = models.IntegerField(db_column='LAEN_ENG_ID')  # Field name made lowercase.
    laen_sort = models.IntegerField(db_column='LAEN_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_eng_new'


class LinkLaMrk(models.Model):
    lam_la_id = models.IntegerField(db_column='LAM_LA_ID')  # Field name made lowercase.
    lam_mrk_id = models.IntegerField(db_column='LAM_MRK_ID')  # Field name made lowercase.
    lam_ga_id = models.IntegerField(db_column='LAM_GA_ID')  # Field name made lowercase.
    lam_sup_id = models.SmallIntegerField(db_column='LAM_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    lam_sort = models.IntegerField(db_column='LAM_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_mrk'


class LinkLaMrkNew(models.Model):
    lamn_la_id = models.IntegerField(db_column='LAMN_LA_ID')  # Field name made lowercase.
    lamn_mrk_id = models.IntegerField(db_column='LAMN_MRK_ID')  # Field name made lowercase.
    lamn_ga_id = models.IntegerField(db_column='LAMN_GA_ID')  # Field name made lowercase.
    lamn_sup_id = models.SmallIntegerField(db_column='LAMN_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    lamn_sort = models.IntegerField(db_column='LAMN_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_mrk_new'


class LinkLaTyp(models.Model):
    lat_typ_id = models.IntegerField(db_column='LAT_TYP_ID')  # Field name made lowercase.
    lat_la_id = models.IntegerField(db_column='LAT_LA_ID')  # Field name made lowercase.
    lat_ga_id = models.IntegerField(db_column='LAT_GA_ID')  # Field name made lowercase.
    lat_sup_id = models.SmallIntegerField(db_column='LAT_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    lat_sort = models.IntegerField(db_column='LAT_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_typ'


class LinkLaTypNew(models.Model):
    latn_sup_id = models.SmallIntegerField(db_column='LATN_SUP_ID', blank=True, null=True)  # Field name made lowercase.
    latn_ga_id = models.IntegerField(db_column='LATN_GA_ID')  # Field name made lowercase.
    latn_typ_id = models.IntegerField(db_column='LATN_TYP_ID')  # Field name made lowercase.
    latn_la_id = models.IntegerField(db_column='LATN_LA_ID')  # Field name made lowercase.
    latn_sort = models.IntegerField(db_column='LATN_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_la_typ_new'


class LinkShoStr(models.Model):
    lss_sho_id = models.SmallIntegerField(db_column='LSS_SHO_ID')  # Field name made lowercase.
    lss_str_id = models.IntegerField(db_column='LSS_STR_ID')  # Field name made lowercase.
    lss_expand = models.SmallIntegerField(db_column='LSS_EXPAND', blank=True, null=True)  # Field name made lowercase.
    lss_level = models.SmallIntegerField(db_column='LSS_LEVEL')  # Field name made lowercase.
    lss_sort = models.SmallIntegerField(db_column='LSS_SORT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_sho_str'


class LinkShoStrType(models.Model):
    lst_str_type = models.SmallIntegerField(db_column='LST_STR_TYPE')  # Field name made lowercase.
    lst_sho_id = models.SmallIntegerField(db_column='LST_SHO_ID')  # Field name made lowercase.
    lst_sort = models.SmallIntegerField(db_column='LST_SORT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_sho_str_type'


class LinkTypEng(models.Model):
    lte_typ_id = models.IntegerField(db_column='LTE_TYP_ID')  # Field name made lowercase.
    lte_nr = models.SmallIntegerField(db_column='LTE_NR')  # Field name made lowercase.
    lte_eng_id = models.IntegerField(db_column='LTE_ENG_ID')  # Field name made lowercase.
    lte_pcon_start = models.IntegerField(db_column='LTE_PCON_START', blank=True,
                                         null=True)  # Field name made lowercase.
    lte_pcon_end = models.IntegerField(db_column='LTE_PCON_END', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_typ_eng'


class LinkTypMrk(models.Model):
    lmk_typ_id = models.IntegerField(db_column='LMK_TYP_ID')  # Field name made lowercase.
    lmk_mrk_id = models.IntegerField(db_column='LMK_MRK_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_typ_mrk'


class Manufacturers(models.Model):
    mfa_id = models.SmallIntegerField(primary_key=True, db_column='MFA_ID')  # Field name made lowercase.
    mfa_pc_mfc = models.SmallIntegerField(db_column='MFA_PC_MFC', blank=True, null=True)  # Field name made lowercase.
    mfa_cv_mfc = models.SmallIntegerField(db_column='MFA_CV_MFC', blank=True, null=True)  # Field name made lowercase.
    mfa_axl_mfc = models.SmallIntegerField(db_column='MFA_AXL_MFC', blank=True, null=True)  # Field name made lowercase.
    mfa_eng_mfc = models.SmallIntegerField(db_column='MFA_ENG_MFC', blank=True, null=True)  # Field name made lowercase.
    mfa_eng_typ = models.SmallIntegerField(db_column='MFA_ENG_TYP', blank=True, null=True)  # Field name made lowercase.
    mfa_mfc_code = models.CharField(db_column='MFA_MFC_CODE', max_length=30, blank=True,
                                    null=True)  # Field name made lowercase.
    mfa_brand = models.CharField(db_column='MFA_BRAND', max_length=60, blank=True,
                                 null=True)  # Field name made lowercase.
    mfa_mf_nr = models.IntegerField(db_column='MFA_MF_NR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'manufacturers'


class ModTypLookup(models.Model):
    mtl_typ_id = models.IntegerField(db_column='MTL_TYP_ID', blank=True, null=True)  # Field name made lowercase.
    mtl_lng_id = models.SmallIntegerField(db_column='MTL_LNG_ID', blank=True, null=True)  # Field name made lowercase.
    mtl_search_text = models.CharField(db_column='MTL_SEARCH_TEXT', max_length=360)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mod_typ_lookup'


class Models(models.Model):
    mod_id = models.IntegerField(primary_key=True, db_column='MOD_ID')  # Field name made lowercase.
    manufacturer = models.ForeignKey(Manufacturers, db_column='MOD_MFA_ID', blank=True,
                                     null=True)  # Field name made lowercase.
    mod_cds_id = models.ForeignKey(CountryDesignations, db_column='MOD_CDS_ID', blank=True,
                                   null=True)  # Field name made lowercase.
    mod_pcon_start = models.IntegerField(db_column='MOD_PCON_START', blank=True,
                                         null=True)  # Field name made lowercase.
    mod_pcon_end = models.IntegerField(db_column='MOD_PCON_END', blank=True, null=True)  # Field name made lowercase.
    mod_pc = models.SmallIntegerField(db_column='MOD_PC', blank=True, null=True)  # Field name made lowercase.
    mod_cv = models.SmallIntegerField(db_column='MOD_CV', blank=True, null=True)  # Field name made lowercase.
    mod_axl = models.SmallIntegerField(db_column='MOD_AXL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'models'


class NumberplatesNl(models.Model):
    nnl_numberplate = models.CharField(db_column='NNL_NUMBERPLATE', max_length=8)  # Field name made lowercase.
    nnl_typ_id = models.IntegerField(db_column='NNL_TYP_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'numberplates_nl'


class Prices(models.Model):
    pri_art_id = models.IntegerField(db_column='PRI_ART_ID')  # Field name made lowercase.
    pri_kv_price_type = models.CharField(db_column='PRI_KV_PRICE_TYPE', max_length=9)  # Field name made lowercase.
    pri_price = models.CharField(db_column='PRI_PRICE', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    pri_kv_price_unit_des_id = models.IntegerField(db_column='PRI_KV_PRICE_UNIT_DES_ID')  # Field name made lowercase.
    pri_kv_quantity_unit_des_id = models.IntegerField(
        db_column='PRI_KV_QUANTITY_UNIT_DES_ID')  # Field name made lowercase.
    pri_val_start = models.DateTimeField(db_column='PRI_VAL_START')  # Field name made lowercase.
    pri_val_end = models.DateTimeField(db_column='PRI_VAL_END', blank=True, null=True)  # Field name made lowercase.
    pri_currency_code = models.CharField(db_column='PRI_CURRENCY_CODE', max_length=9)  # Field name made lowercase.
    pri_rebate = models.CharField(db_column='PRI_REBATE', max_length=15, blank=True,
                                  null=True)  # Field name made lowercase.
    pri_discount_flag = models.SmallIntegerField(db_column='PRI_DISCOUNT_FLAG', blank=True,
                                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prices'


# class SearchTree(models.Model):
#     str_id = models.IntegerField(primary_key=True, db_column='STR_ID')  # Field name made lowercase.
#     str_id_parent = models.IntegerField(db_column='STR_ID_PARENT', blank=True, null=True)  # Field name made lowercase.
#     str_type = models.SmallIntegerField(db_column='STR_TYPE', blank=True, null=True)  # Field name made lowercase.
#     str_level = models.SmallIntegerField(db_column='STR_LEVEL', blank=True, null=True)  # Field name made lowercase.
#     str_des_id = models.IntegerField(db_column='STR_DES_ID', blank=True, null=True)  # Field name made lowercase.
#     str_sort = models.SmallIntegerField(db_column='STR_SORT', blank=True, null=True)  # Field name made lowercase.
#     str_node_nr = models.IntegerField(db_column='STR_NODE_NR', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'search_tree'


class StrLookup(models.Model):
    stl_lng_id = models.SmallIntegerField(db_column='STL_LNG_ID')  # Field name made lowercase.
    stl_search_text = models.CharField(db_column='STL_SEARCH_TEXT', max_length=180)  # Field name made lowercase.
    stl_str_id = models.IntegerField(db_column='STL_STR_ID')  # Field name made lowercase.
    stl_ga_id = models.IntegerField(db_column='STL_GA_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'str_lookup'


class SupersededArticles(models.Model):
    sua_art_id = models.IntegerField(db_column='SUA_ART_ID')  # Field name made lowercase.
    sua_number = models.CharField(db_column='SUA_NUMBER', max_length=66)  # Field name made lowercase.
    sua_sort = models.IntegerField(db_column='SUA_SORT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'superseded_articles'


class SupplierAddresses(models.Model):
    sad_sup_id = models.SmallIntegerField(db_column='SAD_SUP_ID')  # Field name made lowercase.
    sad_type_of_address = models.CharField(db_column='SAD_TYPE_OF_ADDRESS', max_length=9)  # Field name made lowercase.
    sad_cou_id = models.SmallIntegerField(db_column='SAD_COU_ID', blank=True, null=True)  # Field name made lowercase.
    sad_name1 = models.CharField(db_column='SAD_NAME1', max_length=120, blank=True,
                                 null=True)  # Field name made lowercase.
    sad_name2 = models.CharField(db_column='SAD_NAME2', max_length=120, blank=True,
                                 null=True)  # Field name made lowercase.
    sad_street1 = models.CharField(db_column='SAD_STREET1', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    sad_street2 = models.CharField(db_column='SAD_STREET2', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    sad_pob = models.CharField(db_column='SAD_POB', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sad_cou_id_postal = models.SmallIntegerField(db_column='SAD_COU_ID_POSTAL', blank=True,
                                                 null=True)  # Field name made lowercase.
    sad_postal_code_place = models.CharField(db_column='SAD_POSTAL_CODE_PLACE', max_length=24, blank=True,
                                             null=True)  # Field name made lowercase.
    sad_postal_code_pob = models.CharField(db_column='SAD_POSTAL_CODE_POB', max_length=24, blank=True,
                                           null=True)  # Field name made lowercase.
    sad_postal_code_cust = models.CharField(db_column='SAD_POSTAL_CODE_CUST', max_length=24, blank=True,
                                            null=True)  # Field name made lowercase.
    sad_city1 = models.CharField(db_column='SAD_CITY1', max_length=120, blank=True,
                                 null=True)  # Field name made lowercase.
    sad_city2 = models.CharField(db_column='SAD_CITY2', max_length=120, blank=True,
                                 null=True)  # Field name made lowercase.
    sad_tel = models.CharField(db_column='SAD_TEL', max_length=120, blank=True, null=True)  # Field name made lowercase.
    sad_fax = models.CharField(db_column='SAD_FAX', max_length=60, blank=True, null=True)  # Field name made lowercase.
    sad_email = models.CharField(db_column='SAD_EMAIL', max_length=180, blank=True,
                                 null=True)  # Field name made lowercase.
    sad_web = models.CharField(db_column='SAD_WEB', max_length=180, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'supplier_addresses'


class TextModuleTexts(models.Model):
    tmt_id = models.IntegerField(db_column='TMT_ID')  # Field name made lowercase.
    tmt_text = models.TextField(db_column='TMT_TEXT', blank=True, null=True)  # Field name made lowercase.
    tmt_first_2000 = models.CharField(db_column='TMT_FIRST_2000', max_length=4000, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'text_module_texts'


class TextModules(models.Model):
    tmo_id = models.IntegerField(db_column='TMO_ID')  # Field name made lowercase.
    tmo_lng_id = models.SmallIntegerField(db_column='TMO_LNG_ID')  # Field name made lowercase.
    tmo_fixed = models.SmallIntegerField(db_column='TMO_FIXED')  # Field name made lowercase.
    tmo_tmt_id = models.IntegerField(db_column='TMO_TMT_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'text_modules'


class TypCountrySpecifics(models.Model):
    tyc_typ_id = models.IntegerField(db_column='TYC_TYP_ID')  # Field name made lowercase.
    tyc_cou_id = models.SmallIntegerField(db_column='TYC_COU_ID')  # Field name made lowercase.
    tyc_pcon_start = models.IntegerField(db_column='TYC_PCON_START', blank=True,
                                         null=True)  # Field name made lowercase.
    tyc_pcon_end = models.IntegerField(db_column='TYC_PCON_END', blank=True, null=True)  # Field name made lowercase.
    tyc_kw_from = models.IntegerField(db_column='TYC_KW_FROM', blank=True, null=True)  # Field name made lowercase.
    tyc_kw_upto = models.IntegerField(db_column='TYC_KW_UPTO', blank=True, null=True)  # Field name made lowercase.
    tyc_hp_from = models.IntegerField(db_column='TYC_HP_FROM', blank=True, null=True)  # Field name made lowercase.
    tyc_hp_upto = models.IntegerField(db_column='TYC_HP_UPTO', blank=True, null=True)  # Field name made lowercase.
    tyc_ccm = models.IntegerField(db_column='TYC_CCM', blank=True, null=True)  # Field name made lowercase.
    tyc_cylinders = models.SmallIntegerField(db_column='TYC_CYLINDERS', blank=True,
                                             null=True)  # Field name made lowercase.
    tyc_doors = models.SmallIntegerField(db_column='TYC_DOORS', blank=True, null=True)  # Field name made lowercase.
    tyc_tank = models.SmallIntegerField(db_column='TYC_TANK', blank=True, null=True)  # Field name made lowercase.
    tyc_kv_voltage_des_id = models.IntegerField(db_column='TYC_KV_VOLTAGE_DES_ID', blank=True,
                                                null=True)  # Field name made lowercase.
    tyc_kv_abs_des_id = models.IntegerField(db_column='TYC_KV_ABS_DES_ID', blank=True,
                                            null=True)  # Field name made lowercase.
    tyc_kv_asr_des_id = models.IntegerField(db_column='TYC_KV_ASR_DES_ID', blank=True,
                                            null=True)  # Field name made lowercase.
    tyc_kv_engine_des_id = models.IntegerField(db_column='TYC_KV_ENGINE_DES_ID', blank=True,
                                               null=True)  # Field name made lowercase.
    tyc_kv_brake_type_des_id = models.IntegerField(db_column='TYC_KV_BRAKE_TYPE_DES_ID', blank=True,
                                                   null=True)  # Field name made lowercase.
    tyc_kv_brake_syst_des_id = models.IntegerField(db_column='TYC_KV_BRAKE_SYST_DES_ID', blank=True,
                                                   null=True)  # Field name made lowercase.
    tyc_kv_catalyst_des_id = models.IntegerField(db_column='TYC_KV_CATALYST_DES_ID', blank=True,
                                                 null=True)  # Field name made lowercase.
    tyc_kv_body_des_id = models.IntegerField(db_column='TYC_KV_BODY_DES_ID', blank=True,
                                             null=True)  # Field name made lowercase.
    tyc_kv_steering_des_id = models.IntegerField(db_column='TYC_KV_STEERING_DES_ID', blank=True,
                                                 null=True)  # Field name made lowercase.
    tyc_kv_steering_side_des_id = models.IntegerField(db_column='TYC_KV_STEERING_SIDE_DES_ID', blank=True,
                                                      null=True)  # Field name made lowercase.
    tyc_max_weight = models.DecimalField(db_column='TYC_MAX_WEIGHT', max_digits=5, decimal_places=0, blank=True,
                                         null=True)  # Field name made lowercase.
    tyc_kv_model_des_id = models.IntegerField(db_column='TYC_KV_MODEL_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    tyc_kv_axle_des_id = models.IntegerField(db_column='TYC_KV_AXLE_DES_ID', blank=True,
                                             null=True)  # Field name made lowercase.
    tyc_ccm_tax = models.IntegerField(db_column='TYC_CCM_TAX', blank=True, null=True)  # Field name made lowercase.
    tyc_litres = models.DecimalField(db_column='TYC_LITRES', max_digits=6, decimal_places=0, blank=True,
                                     null=True)  # Field name made lowercase.
    tyc_kv_drive_des_id = models.IntegerField(db_column='TYC_KV_DRIVE_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    tyc_kv_trans_des_id = models.IntegerField(db_column='TYC_KV_TRANS_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typ_country_specifics'


class TypVoltages(models.Model):
    tvo_typ_id = models.IntegerField(db_column='TVO_TYP_ID')  # Field name made lowercase.
    tvo_nr = models.SmallIntegerField(db_column='TVO_NR')  # Field name made lowercase.
    tvo_kv_voltage_des_id = models.IntegerField(db_column='TVO_KV_VOLTAGE_DES_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typ_voltages'


class TypWheelBases(models.Model):
    twb_typ_id = models.IntegerField(db_column='TWB_TYP_ID')  # Field name made lowercase.
    twb_nr = models.SmallIntegerField(db_column='TWB_NR')  # Field name made lowercase.
    twb_wheel_base = models.IntegerField(db_column='TWB_WHEEL_BASE')  # Field name made lowercase.
    twb_kv_axle_pos_des_id = models.IntegerField(db_column='TWB_KV_AXLE_POS_DES_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typ_wheel_bases'


class TypeNumbers(models.Model):
    tyn_typ_id = models.IntegerField(db_column='TYN_TYP_ID')  # Field name made lowercase.
    tyn_search_text = models.CharField(db_column='TYN_SEARCH_TEXT', max_length=60)  # Field name made lowercase.
    tyn_kind = models.SmallIntegerField(db_column='TYN_KIND')  # Field name made lowercase.
    tyn_display_nr = models.CharField(db_column='TYN_DISPLAY_NR', max_length=60, blank=True,
                                      null=True)  # Field name made lowercase.
    tyn_gop_nr = models.CharField(db_column='TYN_GOP_NR', max_length=75, blank=True,
                                  null=True)  # Field name made lowercase.
    tyn_gop_start = models.IntegerField(db_column='TYN_GOP_START', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'type_numbers'


class Types(models.Model):
    typ_id = models.IntegerField(primary_key=True, db_column='TYP_ID')  # Field name made lowercase.
    typ_cds_id = models.IntegerField(db_column='TYP_CDS_ID', blank=True, null=True)  # Field name made lowercase.
    typ_mmt_cds_id = models.IntegerField(db_column='TYP_MMT_CDS_ID', blank=True,
                                         null=True)  # Field name made lowercase.
    typ_mod_id = models.IntegerField(db_column='TYP_MOD_ID')  # Field name made lowercase.
    typ_sort = models.IntegerField(db_column='TYP_SORT')  # Field name made lowercase.
    typ_pcon_start = models.IntegerField(db_column='TYP_PCON_START', blank=True,
                                         null=True)  # Field name made lowercase.
    typ_pcon_end = models.IntegerField(db_column='TYP_PCON_END', blank=True, null=True)  # Field name made lowercase.
    typ_kw_from = models.IntegerField(db_column='TYP_KW_FROM', blank=True, null=True)  # Field name made lowercase.
    typ_kw_upto = models.IntegerField(db_column='TYP_KW_UPTO', blank=True, null=True)  # Field name made lowercase.
    typ_hp_from = models.IntegerField(db_column='TYP_HP_FROM', blank=True, null=True)  # Field name made lowercase.
    typ_hp_upto = models.IntegerField(db_column='TYP_HP_UPTO', blank=True, null=True)  # Field name made lowercase.
    typ_ccm = models.IntegerField(db_column='TYP_CCM', blank=True, null=True)  # Field name made lowercase.
    typ_cylinders = models.SmallIntegerField(db_column='TYP_CYLINDERS', blank=True,
                                             null=True)  # Field name made lowercase.
    typ_doors = models.SmallIntegerField(db_column='TYP_DOORS', blank=True, null=True)  # Field name made lowercase.
    typ_tank = models.SmallIntegerField(db_column='TYP_TANK', blank=True, null=True)  # Field name made lowercase.
    typ_kv_voltage_des_id = models.IntegerField(db_column='TYP_KV_VOLTAGE_DES_ID', blank=True,
                                                null=True)  # Field name made lowercase.
    typ_kv_abs_des_id = models.IntegerField(db_column='TYP_KV_ABS_DES_ID', blank=True,
                                            null=True)  # Field name made lowercase.
    typ_kv_asr_des_id = models.IntegerField(db_column='TYP_KV_ASR_DES_ID', blank=True,
                                            null=True)  # Field name made lowercase.
    typ_kv_engine_des_id = models.IntegerField(db_column='TYP_KV_ENGINE_DES_ID', blank=True,
                                               null=True)  # Field name made lowercase.
    typ_kv_brake_type_des_id = models.IntegerField(db_column='TYP_KV_BRAKE_TYPE_DES_ID', blank=True,
                                                   null=True)  # Field name made lowercase.
    typ_kv_brake_syst_des_id = models.IntegerField(db_column='TYP_KV_BRAKE_SYST_DES_ID', blank=True,
                                                   null=True)  # Field name made lowercase.
    typ_kv_fuel_des_id = models.IntegerField(db_column='TYP_KV_FUEL_DES_ID', blank=True,
                                             null=True)  # Field name made lowercase.
    typ_kv_catalyst_des_id = models.IntegerField(db_column='TYP_KV_CATALYST_DES_ID', blank=True,
                                                 null=True)  # Field name made lowercase.
    typ_kv_body_des_id = models.IntegerField(db_column='TYP_KV_BODY_DES_ID', blank=True,
                                             null=True)  # Field name made lowercase.
    typ_kv_steering_des_id = models.IntegerField(db_column='TYP_KV_STEERING_DES_ID', blank=True,
                                                 null=True)  # Field name made lowercase.
    typ_kv_steering_side_des_id = models.IntegerField(db_column='TYP_KV_STEERING_SIDE_DES_ID', blank=True,
                                                      null=True)  # Field name made lowercase.
    typ_max_weight = models.DecimalField(db_column='TYP_MAX_WEIGHT', max_digits=5, decimal_places=0, blank=True,
                                         null=True)  # Field name made lowercase.
    typ_kv_model_des_id = models.IntegerField(db_column='TYP_KV_MODEL_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    typ_kv_axle_des_id = models.IntegerField(db_column='TYP_KV_AXLE_DES_ID', blank=True,
                                             null=True)  # Field name made lowercase.
    typ_ccm_tax = models.IntegerField(db_column='TYP_CCM_TAX', blank=True, null=True)  # Field name made lowercase.
    typ_litres = models.DecimalField(db_column='TYP_LITRES', max_digits=6, decimal_places=0, blank=True,
                                     null=True)  # Field name made lowercase.
    typ_kv_drive_des_id = models.IntegerField(db_column='TYP_KV_DRIVE_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    typ_kv_trans_des_id = models.IntegerField(db_column='TYP_KV_TRANS_DES_ID', blank=True,
                                              null=True)  # Field name made lowercase.
    typ_kv_fuel_supply_des_id = models.IntegerField(db_column='TYP_KV_FUEL_SUPPLY_DES_ID', blank=True,
                                                    null=True)  # Field name made lowercase.
    typ_valves = models.SmallIntegerField(db_column='TYP_VALVES', blank=True, null=True)  # Field name made lowercase.
    typ_rt_exists = models.SmallIntegerField(db_column='TYP_RT_EXISTS', blank=True,
                                             null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'types'


class UtilityDirect(models.Model):
    utd_art_id = models.IntegerField(db_column='UTD_ART_ID')  # Field name made lowercase.
    utd_text = models.CharField(db_column='UTD_TEXT', max_length=2000, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'utility_direct'
