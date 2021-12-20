import sys
# would usually avoid this by restructuring the project using poetry but for simplicity
# and due to time constraints I stuck with this approach
sys.path.append('src')
print(sys.path)
from src.invoice import Invoice


def test_invoice():
    text = "< BankID .Il\n 09:03\n 92 %\n Kontofaktura\n Sida 1/2\n Datum:\n 2018-05-10\n Fakturanummer:\n " \
           "Skuld vid utskick i april:\n 25 688,92 kr\n Inbetalningar:\n - 1 000,00 kr\n " \
           "Nya köp (se baksida):\n 716,00 kr\n 415 85 02-7\n +\n Administrativ avgift:\n 29,00 kr\n 394,19 kr\n " \
           "Ränta:\n Förseningsavgift:\n 135,00 kr\n " \
           "*Om du betalar in ett lägre belopp än 4 346 kr (dock minst 3 659 kr) så\n " \
           "gör du om alla dina köp till villkoren för konto - betala i din egen takt.\n " \
           "=\n Skuld vid forfallodatum:\n 25 963,11 kr\n " \
           "Dina räntevillkor ändras till gällande årsränta som nu är 19,90 %. Effektiv\n " \
           "ränta vid köp om exempelvis 10 000 kr med en administrativ avgift på 29\n " \
           "kr/mån och betalning över 12 månader med 955 kr per månad blir 29,22\n " \
           "%, totalkostnad 11 458 kr.\n 111122223333444\n Stefan Sandpapper\n Stanstuvavägen 10\n 56741 Ankeborg\n " \
           "Sverige\n Att betala denna månad:\n 4 346 kr\n Eller betala valfritt belopp *, från\n 3 659 kr\n " \
           "Oss tillhanda\n 2018-05-30\n Plusgiro\n OCR-nummer\n @ PlusGirot\n INBETALNING/GIRERING CK\n Kod 1\n " \
           "Till PlusGirokonto nr.\n Avgift\n Kassastampel\n 330-5182\n Betalningsmottagare (endast namn)\n Anyfin\n " \
           "Avsändare (namn och postadress)\n " \
           "Om du betalar in ett lägre belopp än 4 346 kr (dock minst 3 659 kr) så gör du\n " \
           "om alla dina köp till villkoren för konto - betala i din egen takt. Dina räntevillkor\n " \
           "ändras till gällande årsränta som nu är 19,90 %. Effektiv ränta vid köp om\n " \
           "exempelvis 10 000 kr med en administrativ avgift på 29 kr/mån och betalning\n " \
           "över 12 månader med 955 kr per månad blir 29,22 %, totalkostnad 11 458 kr.\n " \
           "Eget kontonr. vid girering\n Meddelande till betalningsmottagare kan\n Svenska kronor\n ore\n " \
           "inte lämnas på denna blankett\n #\n # 16#"
    invoice = Invoice(text)
    data = invoice.get_invoice_data()
    assert isinstance(data, dict)
    assert data['customer name'] == 'Stefan Sandpapper'
    assert data['customer address'] == 'Stanstuvavägen 10 56741 Ankeborg Sverige'
    assert isinstance(data['loan fees'], float)
    assert data['payment account'] == '330-5182'