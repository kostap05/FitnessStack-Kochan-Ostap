# FitnessStack-Kochan-Ostap

# 🏋️‍♂️ FitnessTracker

**FitnessTracker** to prosta, ale rozbudowana aplikacja webowa, która pozwala użytkownikom:

 - rejestrować się i logować (autentykacja JWT)
 - zapisywać własne treningi: data, typ, czas, kalorie
 - generować motywacyjne cytaty i plany treningowe z zewnętrznego API  
 - przeglądać statystyki swoich treningów (ilość kalorii, czas, częstotliwość)  
 - zarządzać swoim profilem

---

## ⚙️ **Technologie**

- **Backend:** FastAPI + JWT (OAuth2)
- **Frontend:** HTML, CSS, JS (Vanilla)
- **Baza danych:** SQLite (przykładowo, możesz łatwo zmienić na PostgreSQL)
- **Testy:** Pytest

## 🔑 **Funkcje Backend (FastAPI)**

- **Rejestracja i logowanie** — hasło hashowane, JWT token
- **Autoryzacja** — `Depends(get_current_user)` przy wszystkich chronionych endpointach
- **Treningi** — CRUD dla treningów (data, typ, czas, kalorie)
- **Motywacyjne cytaty** — z zewnętrznego API lub własna kolekcja
- **Statystyki** — obliczanie kalorii w czasie, podsumowania

---

## 🎨 **Funkcje Frontend**

- 📅 **Formularz dodawania treningu** (data, typ, czas)
- 📊 **Tabela wszystkich treningów**
- 💡 **Przycisk „Motywacja”** — wyświetla cytat
- 📈 **(Opcjonalnie) Wykres kalorii z treningów**
- 👤 **Profil użytkownika** — edytowalne dane, awatar
- ✅ **Wspólny navbar na każdej stronie**

---

## 🧪 **Testy**

Przykłady testów Pytest:
 - Rejestracja nowego użytkownika
 - Logowanie i sprawdzenie ważności JWT 
 - Dodawanie treningu (autoryzacja)
 - Sprawdzanie błędów: brak tokena, zły login, dostęp bez uprawnień
 - Obliczenia kalorii w czasie