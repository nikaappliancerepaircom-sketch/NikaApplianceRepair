# Nika Appliance Repair — Project Config

## Site
- **Domain:** nikaappliancerepair.com
- **Type:** Local service business — appliance repair
- **Location:** Toronto, Ontario, Canada
- **Stack:** Static HTML + WordPress (MCP connected)

## SEO Config
- **Primary domain:** nikaappliancerepair.com
- **Target location:** Toronto, Ontario, Canada
- **Location code (DataForSEO):** 1006984
- **Target language:** English
- **Competitors:** appliancerepair.ca, hartmanns.ca, torontoappliance.com
- **Main keywords:** appliance repair toronto, refrigerator repair toronto, washer repair toronto
- **Brands:** LG, Samsung, Whirlpool, Bosch, Frigidaire, Kenmore, GE, Miele

## DataForSEO
- DATAFORSEO_LOGIN=care@boomymarketing.com
- DATAFORSEO_PASSWORD=61268d7d9f0e1681

## SEO Skill
For any SEO task use: `/nika-seo` — it auto-detects context and routes to right tool.

## Satellite Sites — Accounts & Deployment

### 3 сателлита (NAR, NEARY, FIXLIFY)
| Параметр | Значение |
|----------|----------|
| GitHub user | `nikaappliancerepaircom-sketch` |
| GitHub token (в .env) | `GITHUB_TOKEN=<see .env file>` |
| GitHub repos | `nikaappliancerepaircom-sketch/nappliancerepair-com` |
| | `nikaappliancerepaircom-sketch/appliancerepairneary-com` |
| | `nikaappliancerepaircom-sketch/fixlifyservices-com` |
| Vercel email | `nikaappliancerepaircom@gmail.com` |
| Vercel team slug | `nikas-projects-0a53955f` |
| Vercel team ID | `team_rGZDvVE6QH6tiEW89jMEd1al` |
| NAR project ID | `prj_hn3veesPIIs3mF3VEbwzdXt7vVjo` |
| NEARY project ID | `prj_FD761BZQz0XWwgwNnzyDzBjGJZvM` |
| FIXLIFY project ID | `prj_A0WxXGXw98m1vVjZdbbjsVcngkxQ` |

### Локальные пути
- `C:/nappliancerepair/` — nappliancerepair.com
- `C:/appliancerepairneary/` — appliancerepairneary.com
- `C:/fixlifyservices/` — fixlifyservices.com

### Git remote (правильный URL)
```bash
git remote set-url origin https://<GITHUB_TOKEN>@github.com/nikaappliancerepaircom-sketch/nappliancerepair-com.git
```

### Деплой вручную (когда нужно)
```bash
vercel login  # войти под nikaappliancerepaircom@gmail.com
cd /c/nappliancerepair && vercel --prod --yes
cd /c/appliancerepairneary && vercel --prod --yes
cd /c/fixlifyservices && vercel --prod --yes
```

### GitHub Actions secrets (в каждом репо nikaappliancerepaircom-sketch/*)
- `VERCEL_TOKEN` — Vercel OAuth token (обновлять через `vercel login` → auth.json)
- `VERCEL_ORG_ID` — `team_rGZDvVE6QH6tiEW89jMEd1al`
- `VERCEL_PROJECT_ID` — project ID конкретного сайта (см. выше)
- `GOOGLE_INDEXING_SA` — JSON из `.env` файла (GOOGLE_INDEXING_API_KEY) ✅ уже добавлен

### Главный сайт (nikaappliancerepair.com)
- GitHub: `nikaappliancerepaircom-sketch/NikaApplianceRepair`
- Vercel: тот же аккаунт `nikaappliancerepaircom@gmail.com`, project `nika-appliance-repair`
