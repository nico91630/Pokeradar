# PokéRadar — flux d'annonces

Le radar est configuré pour la **revente**, sans plafond de budget. Le fichier `feed.json` est volontairement vide tant qu'aucune source autorisée n'est connectée. **Ne pas inventer d'annonces.**

## Schéma des annonces
```json
{
  "updated_at": "2026-11-01T10:00:00Z",
  "source_status": "connected",
  "items": [
    {
      "url": "https://www.vinted.fr/items/123456789-exemple",
      "title": "Nom et numéro de la carte",
      "source": "Nom de la source autorisée",
      "ask_price": 100,
      "purchase_fees": 5,
      "shipping": 4,
      "market_value": 160,
      "selling_fee_rate": 0.1,
      "resale_shipping": 4,
      "other_costs": 0
    }
  ]
}
```

Toutes les valeurs monétaires sont en EUR. Le `selling_fee_rate` est une fraction (0.1 = 10 %). Les montants doivent provenir d'une source vérifiable; les estimations doivent être présentées comme telles. Le bénéfice potentiel est une approximation, avant fiscalité, retours et autres coûts non renseignés.

## Source des annonces
GitHub Pages ne peut pas rechercher des annonces Vinted en temps réel. Un fournisseur de données autorisé doit alimenter ce JSON via un workflow ou un service externe. Aucun scraper Vinted ni contournement des protections du site n'est fourni.

## Alertes
Les notifications du navigateur sont limitées aux visites actives. Pour recevoir des alertes lorsque l'application est fermée, il faut un service de push ou un bot Telegram, ses identifiants secrets et une source autorisée. Ne jamais placer les jetons Telegram dans ce dépôt public.
