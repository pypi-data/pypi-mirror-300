from ernestas_biudzetas.biudzetas import Biudzetas


biudzetas = Biudzetas()
print(biudzetas.gauti_balansa())
biudzetas.patodyti_ataskaita()
print('kiek irasu', len(biudzetas))


def select_input() -> int:
    """_summary_

    Raises:
        ValueError: if not number or not in [1,2]

    Returns:
        int: 1-pajamos or 2-islaidos
    """
    while True:
        try:
            input_select = int(
                input('Koki irasa norite ivesti:\npajamos/islaidos(1/2): '))
            if input_select not in [1, 2]:
                raise ValueError('neteisingai ivedet')
            return input_select
        except ValueError as err:
            print(f'{err}, bandykite dar karta.')


def validate_input_sum():
    while True:
        try:
            input_sum = float(
                input('Iveskite suma: '))
            return input_sum
        except ValueError:
            print(f'Suma turi buti ivesta skaitmenimis per ".", bandykite dar karta.')


def validate_input_string(text: str):
    while True:
        try:
            input_string = input(text)
            if len(input_string) < 3:
                raise ValueError('Iveskite ne maziau 3 raidziu')
            if len(input_string) > 200:
                raise ValueError(
                    'Per ilgas pavadinimas, ne dauogiau 200 raidziu')
            return input_string
        except ValueError as err:
            print(f'{err}, bandykite dar karta.')


def pajamu_irasai_input():
    # iveskite suma float
    suma = validate_input_sum()

    # ivesti siuntejas string
    siuntejas = validate_input_string('Ivesk siuntejo pavadinima: ')

    # ivesti papildoma_informacija string
    papildoma_info = validate_input_string('Ivesk papildoma informacija: ')

    return {'suma': suma, 'siuntejas': siuntejas, 'papildoma_informacija': papildoma_info}


def islaidu_irasai_input():
    # iveskite suma float
    suma = validate_input_sum()

    # ivesti siuntejas string
    atsiskaitymo_budas = validate_input_string(
        'Ivesk atsiskaitymo buda, pavadinima: ')

    # ivesti papildoma_informacija string
    isigyta_preke_paslauga = validate_input_string(
        'Ivesk isigyta prekes ar paslaugos pavadinima: ')

    return {'suma': suma, 'atsiskaitymo_budas': atsiskaitymo_budas, 'isigyta_preke_paslauga': isigyta_preke_paslauga}


def set_pajamu_irasai(pajamu_input: dict):
    if biudzetas.prideti_pajamu_irasa(pajamu_input['suma'], pajamu_input['siuntejas'], pajamu_input['papildoma_informacija']):
        print("Pajamu irasas sukurtas sekmingai")
        return
    print("Pajamu irasas Nesusikure, bandykite dar")


def set_islaidu_irasai(islaidu_input: dict):
    if biudzetas.y(islaidu_input['suma'], islaidu_input['atsiskaitymo_budas'], islaidu_input['isigyta_preke_paslauga']):
        print("Islaidu irasas sukurtas sekmingai")
        return
    print("Islaidu irasas Nesusikure, bandykite dar")


def is_continue_prog():
    while True:
        try:
            is_continue = input('Ar norite testi ivedima? Taip(Y)/Ne(n)')
            if is_continue == 'Y':
                return True
            if is_continue == 'n':
                print('programa uzbaigta!')
                return False
            raise ValueError('suveskite Y/n')
        except ValueError as err:
            print(f'{err}')


while True:
    choose_type = select_input()
    if choose_type == 1:
        pajamu_input = pajamu_irasai_input()
        set_pajamu_irasai(pajamu_input)

    if choose_type == 2:
        islaidu_input = islaidu_irasai_input()
        set_islaidu_irasai(islaidu_input)

    print('Ataskaita')
    biudzetas.patodyti_ataskaita()

    is_continue = is_continue_prog()
    if is_continue:
        continue
    else:
        break
