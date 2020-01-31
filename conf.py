PLAYERS = ('Repsol', 'Naturgy', 'Powen', 'Aldro', 'Gesternova')
PLAYERS = ('Gesternova',)

URL_REPSOL = 'https://simulador-solify.repsolluzygas.com/'
URL_NATURGY = 'https://productos.naturgy.es/servicios/servisolar/'
URL_POWEN = 'https://powen.es/#simulador'
URL_ALDRO = 'https://calculadora.aldrosolar.com/?tipo=individual'
URL_GESTERNOVA = 'https://contigoenergia.com/calculadora-autoconsumo-solar-2/'

ADDRESSES = (
    'Calle Morcín 2, Asturias', \
    'Calle Magnolio 9, Ávila', \
    'Calle Vitoria 8, Burgos', \
    'Calle San Pedro 3, León', \
    'Calle Mayor 5, Madrid', \
    'Calle Luis Montoto 1, Sevilla'   
)
PROVINCES = tuple(address.split(' ')[-1] for address in ADDRESSES)

MONTHLY_BILLS = ('100', '150', '180', '200', '220', '250', '300', '400', '500')
YEARLY_CONSUMPTIONS = tuple(str(int(int(monthlyBill)*12/0.14)) for monthlyBill in MONTHLY_BILLS)    # €/month = €/month * 12 months/year * kWh/0.14 € = kWh/year
MONTHLY_BILL_RANGES = ('75 - 100', '125 - 150', '175 - 200', '200 - 225', '225 - 250', '275 - 300', '375 - 400', '475 - 500')



COORDS_REPSOL = {
    'Asturias': {
        '1': (610, 510),
        '2': (820, 530),
        '3': (810, 590),
        '4': (600, 570)
    },
    'Ávila': {
        '1': (880, 450),
        '2': (1020, 450),
        '3': (1020, 530),
        '4': (880, 530)
    },
}

COORDS_ALDRO = {
    'Asturias': {
        '1': (600, 580),
        '2': (810, 600),
        '3': (800, 660),
        '4': (590, 640)
    },
    'Ávila': {
        '1': (880, 450),
        '2': (1020, 450),
        '3': (1020, 530),
        '4': (880, 530)
    },
}

COORDS_GESTERNOVA = {
    'Asturias': {
        '1': (590, 730),
        '2': (800, 750),
        '3': (790, 810),
        '4': (580, 790)
    },
    'Ávila': {
        '1': (880, 450),
        '2': (1020, 450),
        '3': (1020, 530),
        '4': (880, 530)
    },
}

PRODUCTION_ESTIMATE = 'productionEstimate'
NUM_PANELS = 'numPanels'
POWER_TOTAL = 'powerTotal'
POWER_PANEL = 'powerPanel'
SAVINGS_PERCENT = 'savingsPercent'
COST_TOTAL = 'costTotal'
COST_MONTHLY_FINANCED = 'costMonthlyFinanced'
SAVINGS_SELF_CONSUMPTION = 'savingsSelfConsumption'
SAVINGS_SELL_BACK = 'savingsSellBack'
SELF_CONSUMPTION_PERCENTAGE = 'selfConsumptionPercentage'
DESCRIPTION_PANEL = 'descriptionPanel'
DESCRIPTION_INVERTER = 'descriptionInverter'
SAVINGS_YEARLY = 'savingsYearly'


