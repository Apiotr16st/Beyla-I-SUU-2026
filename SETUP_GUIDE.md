# Setup Guide

Ten plik opisuje aktualny, działający wariant projektu:

- aplikacja działa w `k3d`
- wdrożony jest stos observability (Grafana Beyla, Prometheus, Grafana)
- serwer MCP działa w Kubernetes
- serwer MCP jest wystawiony lokalnie bez `port-forward`
- lokalny `prompt-service` działa w Dockerze
- `prompt-service` używa Gemini przez `GOOGLE_API_KEY`

## 1. Wymagania

Na komputerze muszą być zainstalowane:

- Docker Desktop
- `kubectl`
- `k3d`
- konto i klucz API do Gemini

## 2. Struktura rozwiązania

Aktualny przepływ wygląda tak:

1. `k3d` uruchamia klaster Kubernetes
2. do klastra wdrażana jest aplikacja `online-boutique`
3. do klastra wdrażany jest stos monitoringu: Prometheus i Beyla (namespace: `observability`) oraz Grafana (namespace: `visualization`)
4. do klastra wdrażany jest `mcp-server`
5. `mcp-server` jest wystawiony na lokalnym porcie `8000`
6. lokalny kontener `prompt-service` wystawia endpoint `POST /prompt` na porcie `8088`
7. `prompt-service` używa Gemini przez `GOOGLE_API_KEY`
8. `prompt-service` łączy się z `mcp-server` i wykonuje narzędzia MCP

## 3. Utworzenie klastra `k3d`

Jeśli klaster już istnieje i chcesz zacząć od czystego stanu:

```powershell
k3d cluster delete beyla-lab
```

Utworzenie klastra:

```powershell
k3d cluster create beyla-lab --agents 1 -p "8000:30080@server:0"
kubectl config use-context k3d-beyla-lab
```

Znaczenie:

- `30080` to `NodePort` usługi MCP w klastrze
- `8000` to lokalny port na hoście
- dzięki temu `mcp-server` będzie dostępny pod `http://localhost:8000`

## 4. Wdrożenie aplikacji

Utwórz namespace aplikacji:

```powershell
kubectl create namespace app
```

Jeśli namespace już istnieje, błąd można zignorować.

Wdróż aplikację:

```powershell
kubectl apply -f .\k8s\app\online-boutique.yaml -n app
```

Sprawdzenie:

```powershell
kubectl get pods -n app
kubectl get deploy -n app
```

## 5. Wdrożenie Observability i Wizualizacji

Wdróż agenta Beyla i bazę Prometheus w dedykowanej przestrzeni nazw:

```powershell
kubectl apply -f .\k8s\observability\
```

Wdróż Grafanę w przestrzeni nazw wizualizacji:

```powershell
kubectl apply -f .\k8s\visualization\
```

Dostęp do dashboardu (zostaw to okno terminala otwarte):

```powershell
kubectl port-forward svc/grafana 3000:80 -n visualization
```

Panel jest dostępny pod adresem `http://localhost:3000`. Dashboard Grafana Beyla został zaimportowany automatycznie.

## 6. Zbudowanie i wdrożenie serwera MCP

Zbuduj obraz:

```powershell
docker build -t mcp-server:latest .\mcp-server -f .\mcp-server\Dockerfile
```

Załaduj obraz do `k3d`:

```powershell
k3d image import mcp-server:latest -c beyla-lab
```

Wdróż MCP:

```powershell
kubectl apply -f .\k8s\mcp\deploy.yaml
```

Jeśli robisz kolejną iterację i zmieniłeś kod serwera:

```powershell
kubectl rollout restart deployment/mcp-server -n mcp
kubectl rollout status deployment/mcp-server -n mcp
```

Sprawdzenie:

```powershell
kubectl get pods -n mcp
kubectl logs -n mcp deployment/mcp-server
```

W logach powinno być:

```text
Uvicorn running on http://0.0.0.0:8000
```

## 7. Sprawdzenie działania MCP lokalnie

`mcp-server` powinien być dostępny lokalnie bez `port-forward` przez:

```text
http://localhost:8000/sse
```

Test klienta MCP:

```powershell
python .\mcp-server\mcp_client.py
```

Powinna pojawić się lista narzędzi:

- `list_deployments`
- `list_pods`
- `scale_deployment`
- `restart_deployment`
- `set_loadgenerator`

## 8. Ustawienie `GOOGLE_API_KEY`

W PowerShell:

```powershell
$env:GOOGLE_API_KEY="twoj_klucz_gemini"
```

Warto sprawdzić, czy zmienna jest ustawiona:

```powershell
echo $env:GOOGLE_API_KEY
```

## 9. Zbudowanie `prompt-service`

Zbuduj obraz:

```powershell
docker build -t prompt-service:latest .\mcp-server -f .\mcp-server\Dockerfile.prompt
```

## 10. Uruchomienie `prompt-service`

Uruchom lokalny kontener:

```powershell
docker run --rm -p 8088:8088 `
  -e GOOGLE_API_KEY=$env:GOOGLE_API_KEY `
  -e MCP_URL=http://host.docker.internal:8000/sse `
  -e GEMINI_MODEL=gemini-2.5-flash `
  prompt-service:latest
```

Znaczenie:

- `8088` to lokalny endpoint HTTP dla promptów
- `MCP_URL` wskazuje na serwer MCP wystawiony lokalnie przez `k3d`
- `GOOGLE_API_KEY` jest używany przez Gemini

## 11. Test `prompt-service`

Health:

```powershell
curl http://localhost:8088/health
```

Prompt:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Wypisz deploymenty w namespace app"}'
```

Aby zobaczyć pełną odpowiedź:

```powershell
$response = Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Wypisz deploymenty w namespace app"}'

$response.answer
```

## 12. Przykładowe prompty

Lista deploymentów:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Wypisz deploymenty w namespace app"}'
```

Restart frontendu:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Zrestartuj frontend w namespace app"}'
```

Skalowanie frontendu:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Sprawdz deploymenty w namespace app i jesli frontend ma mniej niz 3 repliki, przeskaluj go do 3"}'
```

Zmiana loadgeneratora:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Ustaw loadgenerator w namespace app na users 20 i rate 5"}'
```

Testowanie monitoringu (zwiększenie obciążenia):

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8088/prompt `
  -ContentType "application/json" `
  -Body '{"prompt":"Ustaw loadgenerator w namespace app na users 100 i rate 20"}'
```
Prompt służy do wygenerowania nagłego skoku ruchu w aplikacji. Pozwala to zweryfikować, czy Beyla poprawnie przechwytuje dane, a Prometheus i Grafana wyświetlają gwałtowny wzrost na wykresach w czasie rzeczywistym.

## 13. Weryfikacja zmian w Kubernetes

Sprawdzenie deploymentów:

```powershell
kubectl get deploy -n app
```

Sprawdzenie podów:

```powershell
kubectl get pods -n app
```

Szczegóły frontendu:

```powershell
kubectl describe deploy frontend -n app
```

Szczegóły loadgeneratora:

```powershell
kubectl describe deploy loadgenerator -n app
```

## 14. Najczęstsze problemy

### `python .\mcp-server\mcp_client.py` zwraca błąd połączenia

Sprawdź:

```powershell
kubectl get pods -n mcp
kubectl logs -n mcp deployment/mcp-server
```

### `curl http://localhost:8000/sse` nie działa

Najczęstsze przyczyny:

- `k3d` został utworzony bez mapowania `8000:30080`
- `mcp-server` nie działa
- w klastrze działa stary obraz MCP

### `prompt-service` zwraca błąd 500

Sprawdź:

- czy `GOOGLE_API_KEY` jest ustawione
- czy MCP działa pod `http://localhost:8000/sse`
- logi kontenera `prompt-service`