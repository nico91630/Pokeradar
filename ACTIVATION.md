# PokéRadar — activer les annonces et les alertes

Le radar de revente est installé, mais **aucune annonce réelle n'est récupérée tant qu'une source autorisée n'est pas connectée**.

## 1. Source d'annonces

Fournir un flux JSON HTTPS dont vous avez le droit de récupérer et redistribuer les données, conforme à [FEED_FORMAT.md](./FEED_FORMAT.md). Ajouter son URL dans le secret GitHub Actions `AUTHORIZED_FEED_URL`. Si la source exige un jeton Bearer, renseigner `AUTHORIZED_FEED_TOKEN`.

Lien direct : [Secrets Actions](../../settings/secrets/actions)

Le projet n'inclut aucun scraping Vinted ni contournement des protections. Les annonces doivent être fournies par un partenaire, une API autorisée ou une source pour laquelle vous détenez les droits nécessaires.

## 2. Notifications Telegram

Créer un bot avec @BotFather dans Telegram, conserver son jeton privé, lui envoyer un premier message et récupérer son chat ID par un moyen de confiance. Renseigner les secrets GitHub Actions `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID`. Ne jamais mettre ces valeurs dans les fichiers publics, les issues ou le chat.

## 3. Exécuter

Ouvrir l'onglet Actions du dépôt, sélectionner **PokéRadar — actualisation et alertes** puis **Run workflow**. Le workflow s'exécute aussi à chaque heure environ (GitHub Actions peut être retardé, et les workflows planifiés peuvent être suspendus sur des dépôts inactifs).

## 4. Limites

Le radar ne certifie ni les prix ni l'authenticité. Les marges restent indicatives et n'incluent pas la fiscalité ni les coûts inconnus. L'absence de source ou d'identifiants empêche l'alimentation ou les notifications correspondantes. GitHub Actions n'offre pas une surveillance à la seconde.
