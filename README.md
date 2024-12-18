# Analiza i projektowanie obiektowe
Repozytorium w ramach ćwiczeń z zajęć Analiza i projektowanie obiektowe dla grupy ZIISS1-3511IO

### Zaliczenie - Do prof. Wołoszyna przekazane zostaną informacje o zaangażowaniu na ćwiczeniach oraz proponowane oceny:
- 3.5 - uruchomienie i podstawowa znajomość aplikacji
- 4.0 - dodanie nowych zbiorów danych i dokonanie analiz
- 4.5 - rozszerzenie istniejących funkcjonalności
- 5.0 - dodanie i przedstawienie nowych funkcjonalności

## Uruchomienie aplikacji
```
git clone https://github.com/pablitosky/analiza_uek.git
```
### (Opcja 1): Lokalnie - bez dockera i z bazą plików

#### 1. Ustaw folder roboczy i zainstaluj wymagane biblioteki
```
cd analiza_uek/streamlit
pip install -r requirements.txt
```

### 2. Uruchom aplikację
```
streamlit run app.py
```
Oczekiwany rezultat: 
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.30.236.138:8501
```

Po zmianach w kodzie źródłowym należy zapisać plik, a następnie odświeżyć stronę w przeglądarce aby zmiany zostały uwzglednione.

### (Opcja 2): W środowisku kontenerowym - z dockerem i bazą plików minio
Wymagania: `docker compose`

#### 1. Ustaw folder roboczy i uruchom stawianie kontenerów
Za pierwszym uruchomieniem zostaną wybudowane obrazy dockera.
```
cd analiza_uek
docker compose up -d
```

#### 2. Utwórz politykę i klucz dostępu w Minio
1. Używając loginu `minio_admin` i hasła `admin123` zaloguj się na localhost:8001
2. Wejdź w *Buckets* -> *Create Bucket* -> nazwa `data` -> kliknij *Create Bucket*
3. Wejdź w *Access Keys* -> *Create access key* -> Podaj *access key* `EPUGrBPNX` oraz *secret key* `joRpSlfHMPtQ` -> kliknij *Create*
4. Na liście *Access Keys* wejdź w stworzony klucz i w polu *Access Key Policy* wklej zawartość pliku `minio_policy.json`

#### 3. Przejdż do aplikacji na localhost:8501.
Ośwież aplikację i dodaj plik aby przetestować połączenie z MINIO.

Dzięki ustawionemu wolumenowi po zmianach w kodzie aplikacja jedynie wymaga odświeżenia jak w wersji bez dockera.

Wrazie problemów odnośnik do dokumentacji: https://docs.streamlit.io/get-started/installation