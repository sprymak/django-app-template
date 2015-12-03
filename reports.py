import os
import geraldo

from django.conf import settings
from django.utils.translation import ugettext as _
from reportlab.lib import pagesizes, units

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(CURRENT_PATH, 'static', 'sales', 'fonts')


def _get_cache_path(filename):
    import os
    return os.path.join(settings.CACHE_PATH, 'sales', 'spot2d', filename)


class SalesReport(geraldo.Report):
    author = 'John Smith Corporation'
    # cache_status = geraldo.cache.CACHE_BY_QUERYSET
    margin_bottom = 0.5 * units.cm
    margin_left = 2 * units.cm
    margin_right = 0.5 * units.cm
    margin_top = 0.5 * units.cm
    page_size = geraldo.landscape(pagesizes.A4)
    print_if_empty = True
    title = _('Sales')
    additional_fonts = {
        'Mono': os.path.join(FONTS_DIR, 'FreeMono.ttf'),
        'MonoBold': os.path.join(FONTS_DIR, 'FreeMonoBold.ttf'),
        'MonoBoldOblique': os.path.join(FONTS_DIR, 'FreeMonoBoldOblique.ttf'),
        'MonoOblique': os.path.join(FONTS_DIR, 'FreeMonoOblique.ttf'),
        'Sans': os.path.join(FONTS_DIR, 'FreeSans.ttf'),
        'SansBold': os.path.join(FONTS_DIR, 'FreeSansBold.ttf'),
        'SansBoldOblique': os.path.join(FONTS_DIR, 'FreeSansBoldOblique.ttf'),
        'SansOblique': os.path.join(FONTS_DIR, 'FreeSansOblique.ttf'),
        'Serif': os.path.join(FONTS_DIR, 'FreeSerif.ttf'),
        'SerifBold': os.path.join(FONTS_DIR, 'FreeSerifBold.ttf'),
        'SerifBoldItalic': os.path.join(FONTS_DIR, 'FreeSerifBoldItalic.ttf'),
        'SerifItalic': os.path.join(FONTS_DIR, 'FreeSerifItalic.ttf'),
    }
    default_style = {'fontName': 'Sans'}

    groups = [
        geraldo.ReportGroup(attribute_name='invoice.outlet',
            band_header=geraldo.ReportBand(
                height=0.7 * units.cm,
                elements=[
                    geraldo.ObjectValue(attribute_name='invoice.outlet',
                        left=0, top=0.1 * units.cm, width=2.25 * units.cm,
                        get_value=lambda val: val.invoice.outlet.uid,
                        style={'fontName': 'MonoBold', 'fontSize': 12}),
                    geraldo.ObjectValue(attribute_name='invoice.outlet',
                        top=0.1 * units.cm, left=2.5 * units.cm,
                        width=25.0 * units.cm,
                        get_value=lambda val: unicode(val.invoice.outlet),
                        style={'fontName': 'SansBold', 'fontSize': 12}),
                    geraldo.ObjectValue(attribute_name='get_amount',
                        top=0.1 * units.cm, left=19.5 * units.cm,
                        width=3.0 * units.cm,
                        action=geraldo.FIELD_ACTION_SUM,
                        display_format=u'\u03a3 %s',
                        get_text=lambda val: u'%.3f' % val.get_amount(),
                        style={'fontName': 'MonoBold', 'fontSize': 12,
                            'alignment': geraldo.utils.TA_RIGHT}),
                ],
                borders={'bottom': True},
            )
        ),
    ]

    class band_detail(geraldo.ReportBand):
        height = 0.5 * units.cm
        elements = (
            geraldo.ObjectValue(attribute_name='product.uid',
                left=0.5 * units.cm, width=2.5 * units.cm,
                style={'fontName': 'Mono'}),
            geraldo.ObjectValue(attribute_name='product',
                left=3.5 * units.cm, width=7.0 * units.cm),
            geraldo.ObjectValue(attribute_name='invoice.shipment_date',
                left=11.0 * units.cm, width=2.25 * units.cm),
            geraldo.ObjectValue(attribute_name='invoice.uid',
                left=13.5 * units.cm, width=2.25 * units.cm),
            geraldo.ObjectValue(attribute_name='quantity',
                left=16.25 * units.cm, width=3.0 * units.cm,
                style={'fontName': 'Mono',
                    'alignment': geraldo.utils.TA_RIGHT}),
            geraldo.ObjectValue(attribute_name='get_amount',
                left=19.5 * units.cm, width=3.0 * units.cm,
                style={'fontName': 'Mono',
                    'alignment': geraldo.utils.TA_RIGHT}),
        )

    class band_page_header(geraldo.ReportBand):
        height = 1.3 * units.cm
        elements = [
            geraldo.SystemField(
                expression=_('%(report_title)s from %(var:min_date)s till '
                    ' %(var:max_date)s'),
                top=0.1 * units.cm, left=0, width=geraldo.BAND_WIDTH,
                style={
                    'fontName': 'SerifBold',
                    'fontSize': 14,
                    'alignment': geraldo.utils.TA_CENTER
                }),
            geraldo.Label(text=_("ID"), top=0.8 * units.cm,
                left=0, width=2.5 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
            geraldo.Label(text=_("Name"), top=0.8 * units.cm,
                left=3.6 * units.cm, width=3.5 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
            geraldo.Label(text=_("Shipping Date"), top=0.8 * units.cm,
                left=11.0 * units.cm, width=2.25 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
            geraldo.Label(text=_("Invoice"), top=0.8 * units.cm,
                left=13.25 * units.cm, width=2.25 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
            geraldo.Label(text=_("Qty"), top=0.8 * units.cm,
                left=16.25 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
            geraldo.Label(text=_("Amount"), top=0.8 * units.cm,
                left=19.5 * units.cm, width=5.75 * units.cm,
                style={'alignment': geraldo.utils.TA_CENTER}),
        ]
        borders = {'bottom': True}

    class band_page_footer(geraldo.ReportBand):
        height = 0.5 * units.cm
        elements = [
            geraldo.SystemField(expression='Created @%(current_datetime)s',
                top=0.1 * units.cm, width=geraldo.BAND_WIDTH, left=0),
            geraldo.SystemField(expression='Page # %(page_number)d '
                    'of %(page_count)d',
                top=0.1 * units.cm, width=geraldo.BAND_WIDTH,
                style={'alignment': geraldo.utils.TA_RIGHT}),
        ]
        borders = {'top': True}

    class band_summary(geraldo.ReportBand):
        height = 1.7 * units.cm
        elements = [
            geraldo.Label(text=_('Records printed:'),
                top=0.1 * units.cm, left=0.5 * units.cm),
            geraldo.ObjectValue(expression='count(uid)',
                left=3.6 * units.cm, width=3.0 * units.cm,
                style={'fontName': 'MonoBold', 'fontSize': 12,
                    'alignment': geraldo.utils.TA_RIGHT}),
            geraldo.ObjectValue(expression='sum(quantity)',
                top=0.6 * units.cm, left=16.25 * units.cm,
                width=3.0 * units.cm,
                display_format=u'\u03a3 %s',
                style={'fontName': 'MonoBold', 'fontSize': 12,
                    'alignment': geraldo.utils.TA_RIGHT}),
            geraldo.ObjectValue(expression='sum(get_amount)',
                top=0.1 * units.cm, left=19.5 * units.cm,
                width=3.75 * units.cm,
                display_format=u'\u03a3 %s',
                style={'fontName': 'MonoBold', 'fontSize': 12,
                    'alignment': geraldo.utils.TA_RIGHT}),
        ]
        borders = {'top': True}
