# Local Opportunity Radar (Kashmir-Only) — LOR-K

## 0. One-line positioning
“Opportunities you are ACTUALLY eligible for — before others even see them.”

## 1. Core Problem
People miss income because notices are scattered (JKSSB, DC office PDFs, boards, WhatsApp) and eligibility details are confusing. Info arrives late or is drowned in noise.

## 2. Inputs Scanned
- **Government Sources**: JKSSB notices, DC office PDFs, District tender boards, Panchayat/municipality postings.
- **NGOs**: Semi-official NGO bulletin PDFs.
- **Academic**: College/institute circulars, Skill mission posts.
- **Informal (Critical)**: WhatsApp group forwards, Telegram channels, Image notices (OCR-enabled).

## 3. Eligibility Engine (Killer Feature)
Classifies opportunities against local user profile:
- **✅ Eligible**: Match all criteria.
- **⚠️ Borderline**: Action needed (e.g., certificate required).
- **❌ Not Eligible**: Hidden/Filtered out.

### User Profile Parameters (Stored Locally)
- District
- Education
- Category
- Age
- Skills
- Availability (seasonal)

## 4. Daily Flow
Morning (5 minutes): User runs `lor.today`.
Output: 3–7 real opportunities. Zero spam. Zero motivation talk.

## 7. Why Competitors Cannot Easily Copy This
- **Requires local cultural parsing**: Understanding nuances in DC office circulars and informal local language.
- **Needs informal channels**: Accessing and processing WhatsApp OCR and forwarded images.
- **Trust depends on accuracy, not volume**: SaaS job portals prioritize volume to show "active" status; LOR-K prioritizes the **negative space** (hiding jobs) to ensure 100% relevance.
- **Local Exclusivity**: Building trust on the ground in a high-friction environment.

## 8. Revenue Model
- **A. Daily Pass**: ₹20/day (Cash-friendly, perfect for immediate utility)
- **B. Monthly**: ₹399/month (Main revenue driver)
- **C. Commission Mode**: 5–10% on success (NGO hires, contract wins)
- **D. Institutional**: Bulk licenses for coaching centers and NGOs.

## 11. Standard Sourcing Protocol (Mandatory)

**Always aggregate from these sources when scanning for J&K jobs:**

### Primary Sources (RSS/API)
- **Google News RSS**: `news.google.com/rss/search?q=<query>&hl=en-IN&gl=IN&ceid=IN:en`
  - Queries: `JKSSB recruitment`, `JKPSC notification`, `Jammu Kashmir jobs vacancy`, `Kashmir Health teacher recruitment`

### Official Government
- **JKSSB**: jkssb.nic.in
- **JKPSC**: jkpsc.nic.in

### News Outlets (Kashmir-specific)
- **Greater Kashmir**: greaterkashmir.com
- **Rising Kashmir**: risingkashmir.com
- **Kashmir Life**: kashmirlife.net
- **Kashmir Indepth**: kashmirindepth.com

### Job Aggregators (National)
- **Adda247**: adda247.com
- **Jagran Josh**: jagranjosh.com
- **Career Power**: careerpower.in
- **FreeJobAlert**: freejobalert.com
- **Physics Wallah**: pw.live (Jobs section)

### Informal Channels
- **JKAlerts**: jkalerts.com (Primary local aggregator)
- **Telegram**: @JKUpdates, @GreaterKashmir (when accessible)
- **WhatsApp Groups**: DC Office forwards, Community pages

### Fetch Pattern
```
1. Google News RSS (4 parallel queries: JKSSB, JKPSC, J&K jobs, Kashmir recruitment)
2. Parse XML → Extract titles, dates, sources
3. Deduplicate by title similarity
4. Filter by date (last 60 days default)
5. Run through Eligibility Engine
6. Output ranked report
```

This protocol is **mandatory** for all `lor.today` and `lor.week` commands.

### All Kashmir Districts (UT-wide Coverage)
- **Government**: JKSSB, JKPSC, J&K Police Recruitment Board, Dept. of Labour & Employment, Universities, Health/Education/PWD/PDD departmental notices.
- **Aggregators**: JKAlerts, JKADWorld.
- **National Portals**: Indeed, LinkedIn, Shine.

### District-Specific (Local Sourcing & Private Visibility)
- **Srinagar**: Secretariat/Directorate notices, Universities, IT services, Hotels. (Sources: LinkedIn, Indeed, Local Telegram/Insta).
- **Anantnag**: Education/Health institutes, Coaching centers. (Sources: FB/Insta job pages, Local newspapers).
- **Baramulla**: Healthcare, Logistics, Trade services. (Sources: Local WhatsApp/Telegram, JKAlerts).
- **Kupwara**: Education, NGOs, Army/Contractual supply tenders. (Sources: Community pages, Employment Exchange).
- **Budgam**: Agri-allied, Small industries, Construction. (Sources: OLX, Local classifieds).
- **Pulwama**: Agri, MSMEs, Factories. (Sources: FB groups, Local recruiters).
- **Shopian**: Horticulture/Agri, Cold storage. (Sources: Community pages, Social media).
- **Kulgam**: Schools, Health centers, Private enterprises. (Sources: Social media, Employment Exchange).
- **Ganderbal**: Central University notices, Education. (Sources: University websites, JKAlerts).
- **Bandipora**: Fisheries, Power projects, NGOs. (Sources: Community pages, Dept notices).

### Practical Takeaway
- **Government Jobs**: UT-wide (JKSSB/JKPSC).
- **Private Jobs**: District-specific (Schools, Hospitals, MSMEs).
- **Fastest Coverage**: JKSSB + JKAlerts + Local Telegram/Instagram channels.
