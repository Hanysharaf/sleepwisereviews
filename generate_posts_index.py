"""Generate /posts/index.html — Level 1 of the topic browse (Spec 009).

12 category cards + cross-category search. No inline article lists.
Article browsing happens on /posts/category/<slug>.html (Spec 009 Level 2 —
see generate_category_pages.py).
"""
import datetime
import json
import os
import re

POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
BASE_URL = 'https://sleepwisereviews.com/posts/'

EXCLUDED = {'index'}

CATEGORIES = {
    'Insomnia & CBT-I': ['insomnia-types', 'cbt-i-guide', 'sleep-anxiety-techniques', 'sleep-when-anxious', 'sleep-disorders-overview', 'sleep-paralysis-explained', 'sleep-ptsd', 'rem-behavior-disorder', 'rem-rebound-explained', 'best-mattress-insomnia', 'best-sleep-supplement-anxiety', 'best-magnesium-for-sleep-anxiety'],
    'Sleep Science': ['sleep-stages-explained', 'circadian-rhythm-basics', 'chronobiology-basics', 'adenosine-sleep-drive', 'sleep-genetics', 'brain-during-sleep', 'dreams-science', 'deep-sleep-benefits', 'rem-sleep-benefits', 'light-sleep-importance', 'sleep-memory-learning', 'sleep-immune-system'],
    'Caffeine & Nutrition': ['caffeine-half-life-sleep', 'blue-light-melatonin', 'melatonin-guide', 'alcohol-sleep-quality', 'sleep-food-connection', 'magnesium-deficiency-sleep', 'magnesium-types-sleep', 'natural-sleep-aids', 'sleep-fasting', 'sleep-hydration', 'sleep-hydration-guide', 'sleep-and-alcohol-free', 'gut-microbiome-sleep', 'sleep-and-thyroid', 'sleep-and-gut-health'],
    'Sleep Environment': ['bedroom-temperature-sleep', 'sleep-environment-optimization', 'sleep-sanctuary-guide', 'bedroom-plants-sleep', 'bedroom-tech-sleep', 'sleep-screen-detox', 'sleep-temperature-regulation', 'sleep-light-therapy', 'altitude-sleep', 'sleep-camping', 'best-blackout-curtain-liner'],
    'Health Conditions': ['sleep-apnea-warning-signs', 'sleep-apnea-diagnosis', 'home-sleep-apnea-test', 'snoring-causes-fixes', 'restless-legs-syndrome', 'sleep-chronic-pain', 'sleep-fibromyalgia', 'sleep-and-pain', 'sleep-depression', 'sleep-mental-health', 'sleep-heart-health', 'sleep-and-diabetes', 'sleep-and-alzheimers', 'sleep-autism-spectrum', 'bad-mattress-health-effects', 'sleep-after-surgery', 'sleep-skin-health', 'sleep-after-covid', 'best-mouthguard-teeth-grinding', 'best-cpap-mask-side-sleepers', 'best-pillow-for-cervical-spondylosis', 'best-mattress-fibromyalgia', 'best-anti-snoring-pillow', 'best-cpap-humidifier', 'best-pillow-for-side-sleepers-shoulder-pain', 'best-cpap-machine-travel', 'best-mattress-sciatica', 'best-mattress-migraines', 'best-mattress-diabetes', 'best-mattress-plantar-fasciitis', 'best-mattress-copd', 'best-mattress-anxiety', 'best-mattress-pcos', 'best-mattress-endometriosis', 'best-mattress-depression', 'best-mattress-heart-failure', 'best-mattress-obesity', 'best-mattress-long-covid', 'best-mattress-ptsd', 'best-mattress-adhd', 'best-mattress-asthma', 'best-mattress-bipolar', 'best-mattress-autism', 'best-mattress-ibs', 'best-mattress-interstitial-cystitis', 'best-mattress-hypothyroidism', 'best-mattress-cancer-treatment', 'best-mattress-epilepsy', 'best-mattress-osteoarthritis', 'best-mattress-gout', 'best-mattress-hiv-aids', 'best-mattress-stroke-recovery', 'best-mattress-multiple-chemical-sensitivity', 'best-mattress-kidney-disease', 'best-mattress-copd-overlap', 'best-mattress-inflammatory-bowel-disease', 'best-mattress-spinal-cord-injury', 'best-mattress-alzheimers-dementia', 'best-mattress-traumatic-brain-injury', 'best-mattress-psoriatic-arthritis', 'best-mattress-type1-diabetes', 'best-mattress-sickle-cell-disease', 'best-mattress-lupus-nephritis', 'best-mattress-chronic-pain', 'best-mattress-hypermobile-eds', 'best-mattress-stiff-person-syndrome', 'best-mattress-complex-sleep-apnea', 'best-mattress-mast-cell-activation', 'best-mattress-pots-syndrome', 'best-mattress-sibo', 'best-mattress-cidp', 'best-mattress-reactive-arthritis', 'best-mattress-burning-mouth-syndrome', 'best-mattress-kleine-levin-syndrome', 'best-mattress-idiopathic-hypersomnia', 'best-mattress-non24-sleep-disorder', 'best-mattress-upper-crossed-syndrome', 'best-mattress-lower-crossed-syndrome', 'best-mattress-patellar-tendinopathy', 'best-mattress-shin-splints', 'best-mattress-rotator-cuff-tear', 'best-mattress-achilles-rupture-recovery', 'best-mattress-hamstring-tendinopathy', 'best-mattress-iliotibial-band-syndrome', 'best-mattress-hip-labral-tear', 'best-mattress-stress-fracture', 'best-mattress-meniscus-tear', 'best-mattress-acl-reconstruction-recovery', 'best-mattress-shoulder-labral-tear', 'best-mattress-nerve-impingement', 'best-mattress-rib-fracture-recovery', 'best-mattress-wrist-fracture-recovery', 'best-mattress-ankle-fracture-recovery', 'best-mattress-hip-fracture-recovery', 'best-mattress-post-spinal-fusion', 'best-mattress-shoulder-replacement-recovery', 'best-mattress-bunion-surgery-recovery', 'best-mattress-cervical-radiculopathy', 'best-mattress-lumbar-radiculopathy', 'best-mattress-vertebral-compression-fracture', 'best-mattress-whiplash', 'best-mattress-knee-cartilage-repair', 'best-mattress-plantar-plate-injury', 'best-mattress-thoracic-spine-pain', 'best-mattress-coccydynia', 'best-mattress-lymphedema', 'best-mattress-pelvic-girdle-pain', 'best-mattress-myofascial-pain-syndrome', 'best-mattress-discogenic-pain', 'best-mattress-spasticity', 'best-mattress-ehlers-danlos-vascular', 'best-mattress-night-terrors', 'best-mattress-sleep-bruxism', 'best-mattress-chronic-sinusitis', 'best-mattress-psoriasis', 'best-mattress-pots', 'best-mattress-lyme-disease', 'best-mattress-mcas', 'best-mattress-als', 'best-mattress-huntingtons-disease', 'best-mattress-cerebral-palsy', 'best-mattress-muscular-dystrophy', 'best-mattress-sleep-apnea', 'best-mattress-narcolepsy', 'best-mattress-crohns-disease', 'best-mattress-osteoporosis', 'best-mattress-tourette-syndrome', 'best-mattress-pelvic-floor-dysfunction', 'best-mattress-dysautonomia', 'best-mattress-raynauds', 'best-mattress-celiac-disease', 'best-mattress-tinnitus', 'best-mattress-chronic-hives', 'best-mattress-hashimotos', 'best-mattress-sjogrens-syndrome', 'best-mattress-polymyalgia-rheumatica', 'best-mattress-bursitis', 'best-mattress-complex-regional-pain-syndrome', 'best-mattress-gastroparesis', 'best-mattress-sleep-paralysis', 'best-mattress-guillain-barre', 'best-mattress-dermatomyositis', 'best-mattress-phantom-limb-pain', 'best-mattress-morton-neuroma', 'best-mattress-cluster-headaches', 'best-mattress-post-mastectomy', 'best-mattress-post-concussion-syndrome', 'best-mattress-hiatal-hernia', 'best-mattress-cauda-equina-syndrome', 'best-mattress-myelomeningocele', 'best-mattress-raynaud-phenomenon', 'best-mattress-hyperparathyroidism', 'best-mattress-cushing-syndrome', 'best-mattress-temporal-arteritis', 'best-mattress-acromegaly', 'best-mattress-addisons-disease', 'best-mattress-polycythemia-vera', 'best-mattress-wilson-disease', 'best-mattress-hemochromatosis', 'best-mattress-porphyria', 'best-mattress-pheochromocytoma', 'best-mattress-amyloidosis', 'best-mattress-systemic-sclerosis', 'best-mattress-eosinophilic-esophagitis', 'best-mattress-pulmonary-hypertension', 'best-mattress-graves-disease', 'best-mattress-myelofibrosis', 'best-mattress-primary-aldosteronism', 'best-mattress-eczema', 'best-mattress-vertigo', 'best-mattress-perimenopause', 'best-mattress-menieres-disease', 'best-mattress-hidradenitis-suppurativa', 'best-mattress-rosacea', 'best-mattress-peripheral-artery-disease', 'best-mattress-complex-regional-pain', 'best-mattress-sacroiliac-joint-pain', 'best-mattress-costochondritis', 'best-mattress-interstitial-lung-disease', 'best-mattress-ehlers-danlos-classical', 'best-mattress-spinal-stenosis-cervical', 'best-mattress-marfan-syndrome', 'best-mattress-osteogenesis-imperfecta', 'best-mattress-scleroderma', 'best-mattress-thoracic-outlet-syndrome', 'best-mattress-avascular-necrosis-hip', 'best-mattress-temporomandibular-joint-disorder', 'best-mattress-shoulder-impingement', 'best-mattress-piriformis-syndrome', 'best-mattress-venous-insufficiency', 'best-mattress-post-laminectomy-syndrome', 'best-mattress-myasthenia-gravis', 'best-mattress-hemophilia', 'best-mattress-knee-pain', 'best-mattress-frozen-shoulder', 'best-mattress-carpal-tunnel-syndrome', 'best-mattress-polymyositis', 'best-mattress-spondylolisthesis', 'best-mattress-meralgia-paresthetica', 'best-mattress-achilles-tendinopathy', 'best-mattress-patellofemoral-syndrome', 'best-mattress-cubital-tunnel-syndrome', 'best-mattress-trigeminal-neuralgia', 'best-mattress-pudendal-neuralgia', 'best-mattress-lateral-epicondylitis', 'best-mattress-golfers-elbow', 'best-mattress-de-quervain-tenosynovitis', 'best-mattress-tarsal-tunnel-syndrome', 'best-mattress-small-fiber-neuropathy', 'best-mattress-intracranial-hypertension', 'best-mattress-arachnoiditis', 'best-mattress-occipital-neuralgia', 'best-mattress-metatarsalgia', 'best-mattress-charcot-marie-tooth', 'best-mattress-syringomyelia', 'best-mattress-thoracic-hyperkyphosis', 'best-mattress-hyperhidrosis', 'best-mattress-periodic-limb-movement', 'best-mattress-central-sensitization', 'best-mattress-lipedema', 'best-mattress-herniated-disc', 'best-mattress-back-pain', 'best-mattress-chronic-back-pain', 'best-mattress-side-sleeper-shoulder-pain', 'best-mattress-scoliosis', 'best-mattress-neck-pain', 'best-mattress-snoring', 'best-mattress-acid-reflux', 'best-mattress-insomnia', 'best-mattress-spinal-stenosis', 'best-mattress-degenerative-disc', 'best-mattress-stomach-sleepers-back-pain', 'best-mattress-stomach-sleepers-lower-back-pain', 'best-mattress-neuropathy', 'best-mattress-chronic-fatigue', 'best-mattress-lupus', 'best-mattress-multiple-sclerosis', 'best-mattress-ankylosing-spondylitis', 'best-mattress-ehlers-danlos', 'best-mattress-rheumatoid-arthritis', 'best-mattress-restless-legs', 'best-mattress-parkinsons'],
    'Life Stages': ['best-mattress-college-students', 'best-mattress-petite-sleeper', 'best-mattress-heavy-sleepers', 'best-mattress-studio-apartment', 'best-mattress-bunk-beds', 'best-mattress-college-dorm', 'best-mattress-rv', 'best-mattress-murphy-bed', 'best-mattress-daybed', 'best-mattress-trundle-bed', 'best-mattress-overheating-pregnancy', 'best-mattress-tall-person', 'best-mattress-teenager', 'best-mattress-teen-athlete', 'best-mattress-newlyweds', 'best-mattress-postpartum', 'best-mattress-knee-replacement', 'best-mattress-hip-replacement', 'best-mattress-overweight', 'best-mattress-kids', 'best-mattress-pregnancy', 'pregnancy-sleep-guide', 'kids-sleep-guide', 'kids-screen-time-sleep', 'teen-sleep-guide', 'aging-and-sleep', 'women-sleep-differences', 'menopause-sleep', 'sleep-menstrual-cycle', 'sleep-new-baby', 'couples-sleep-problems', 'best-pregnancy-pillows', 'best-pregnancy-pillow-back-pain', 'best-body-pillow', 'best-body-pillow-side-sleepers', 'best-white-noise-machine-baby', 'best-crib-mattress', 'best-toddler-pillow', 'best-baby-monitor-sleep', 'best-weighted-blanket-kids', 'best-kids-alarm-clock', 'best-mattress-seniors', 'best-mattress-for-seniors', 'best-mattress-topper-seniors', 'best-cooling-pillow-menopause'],
    'Timing & Jet Lag': ['reset-sleep-schedule', 'jet-lag-guide', 'sleep-travel-tips', 'sleep-business-travel', 'social-jetlag', 'daylight-saving-sleep', 'shift-work-shift', 'night-shift-optimization', 'polyphasic-sleep', 'polyphasic-sleep-schedules', 'sleep-consistency-importance', 'weekend-sleep-mistake', 'wrong-sleeping-in-weekends', 'shift-work-sleep', 'best-travel-pillow'],
    'Napping & Performance': ['power-nap-science', 'napping-science', 'sleep-inertia', 'microsleep-dangers', 'sleep-athletic-performance', 'sleep-exercise-timing', 'sleep-productivity', 'sleep-goal-setting', 'sleep-longevity', 'sleep-creativity', 'sleep-mental-performance'],
    'Guides & Plans': ['ultimate-sleep-guide', 'sleep-hygiene-checklist', 'wind-down-routine', 'morning-habits-sleep', 'sleep-journal-guide', '30-day-sleep-challenge', 'sleep-debt-accumulation', 'sleep-debt-recovery', 'summer-sleep-guide', 'winter-sleep-guide', 'sleep-exam-study', 'sleep-tracking-worth-it', 'sleep-tracking-data', 'hypnic-jerk-explained', 'lucid-dreaming-guide', 'sleep-myth-8-hours', 'sleep-myths-series', 'sleep-quality-vs-quantity', 'waking-at-3am', 'sleep-chronotypes', 'morning-lark-night-owl', 'sleep-cortisol-stress', 'sleep-and-hormones', 'sleep-loneliness', 'sleep-grief', 'sleep-adhd', 'sleep-and-weight-loss', 'does-sex-before-bed-help-sleep', 'sex-and-sleep-intimacy-quality', 'how-much-sleep-do-i-need', 'how-to-fall-asleep-fast', 'best-sleep-position', 'best-bath-soak-sleep', 'best-overnight-face-mask', 'sleep-myth-older-people-less-sleep'],
    'Mattresses & Bedding': ['best-mattresses-back-pain', 'best-mattresses-couples-2026', 'best-mattress-toppers', 'best-cooling-mattress-pads', 'best-cooling-pillows', 'best-cooling-pillow-hot-sleepers', 'best-cooling-sheets', 'best-linen-sheets', 'best-bamboo-sheets', 'best-mattress-stomach-sleepers', 'best-mattress-side-sleepers', 'best-mattress-back-sleepers', 'best-pillow-sleep-position', 'best-pillow-side-sleepers', 'best-pillow-neck-pain', 'best-grounding-sheets', 'best-memory-foam-pillow', 'mattress-buying-guide', 'memory-foam-vs-hybrid-mattress', 'latex-vs-memory-foam-mattress', 'best-mattresses-under-500', 'best-smart-mattresses', 'best-latex-mattress', 'best-natural-latex-mattress', 'best-duvet-insert', 'best-mattress-protector', 'best-cooling-mattress-topper', 'best-silk-pillowcase', 'best-adjustable-bed-frame', 'best-cooling-comforter', 'best-down-alternative-comforter', 'best-mattress-pad', 'best-pillow-back-sleepers', 'best-pillow-stomach-sleepers', 'best-hotel-pillow', 'best-buckwheat-pillow', 'best-contour-pillow', 'best-water-pillow', 'best-latex-pillow', 'best-organic-mattress', 'best-split-king-adjustable-base', 'best-mattress-topper-back-pain', 'best-mattress-night-sweats', 'best-mattress-menopause', 'best-mattress-firm-vs-medium', 'best-mattress-hot-sleepers', 'best-adjustable-pillow', 'best-foam-mattress-under-500', 'best-mattress-pressure-relief', 'best-mattress-heavy-people', 'best-pillow-shoulder-pain', 'best-bed-frame-heavy-person', 'best-mattress-topper-hot-sleepers', 'best-adjustable-base-bed-frame', 'best-mattress-adjustable-base', 'best-mattress-back-pain-side-sleeper', 'best-mattress-shoulder-pain', 'best-mattress-hip-pain', 'best-mattress-arthritis', 'best-heated-mattress-pad', 'best-cervical-pillow', 'best-mattress-topper-memory-foam', 'best-latex-mattress-topper', 'best-bamboo-pillow', 'best-waterproof-mattress-protector', 'best-feather-pillow', 'best-percale-sheets', 'best-tencel-sheets', 'best-sateen-sheets', 'best-flannel-sheets', 'best-cooling-mattress-pad', 'best-down-pillow', 'best-silk-sheets', 'best-linen-duvet-cover', 'best-bamboo-mattress-topper', 'best-cooling-sheets-for-night-sweats', 'best-organic-cotton-sheets', 'best-mattress-under-1000', 'best-duvet-insert-for-hot-sleepers', 'best-pillow-for-stomach-sleepers-neck-pain', 'best-murphy-bed-mattress', 'best-bed-in-a-box', 'best-hybrid-mattress', 'best-innerspring-mattress', 'best-mattress-topper-side-sleepers', 'best-weighted-blanket', 'best-white-noise-machine', 'best-memory-foam-mattress', 'best-cooling-pillow', 'best-king-size-mattress', 'best-firm-mattress', 'best-queen-size-mattress', 'best-pillow-top-mattress', 'best-plush-mattress', 'best-twin-xl-mattress', 'best-mattress-guest-room', 'best-twin-mattress', 'best-mattress-twin-xl', 'best-queen-mattress', 'best-king-mattress', 'best-california-king-mattress', 'best-full-size-mattress', 'best-mattress-heavy-side-sleepers', 'best-cooling-mattress-hot-sleepers', 'best-mattress-couples-different-preferences', 'best-adjustable-mattress', 'best-mattress-petite-side-sleepers', 'best-mattress-combination-sleepers', 'best-mattress-restless-sleeper', 'best-mattress-lower-back-pain-side-sleepers', 'best-mattress-under-200', 'best-mattress-under-300', 'best-mattress-under-500', 'best-mattress-topper', 'best-cooling-mattress', 'best-full-mattress', 'best-futon-mattress', 'best-mattress-couples', 'best-mattress-athlete', 'best-mattress-shift-workers', 'best-mattress-no-box-spring', 'best-mattress-platform-bed'],
    'Sleep Products': ['best-sleep-masks', 'best-sleep-mask', 'best-blackout-curtains', 'best-humidifiers-sleep', 'best-sleep-headphones', 'article-white-noise-machines', 'best-white-noise-machines-sleeping', 'best-light-therapy-lamps', 'best-blue-light-glasses', 'best-aromatherapy-sleep', 'best-cpap-alternatives', 'article-weighted-blanket', 'best-anti-snoring-devices', 'best-sleep-monitors', 'best-sleep-apps', 'best-sleep-tracking-rings', 'best-earplugs-sleeping', 'best-sunrise-alarm-clocks', 'best-weighted-blankets-adults', 'best-knee-pillow', 'best-bed-wedge-pillow', 'best-lumbar-support-pillow', 'best-alarm-clock-heavy-sleepers', 'best-electric-blanket', 'best-cpap-pillow', 'best-air-purifier-sleep', 'best-sleep-tracking-smartwatch', 'best-sleep-headphones-side-sleepers', 'best-weighted-blanket-anxiety', 'best-foot-warmer-bed', 'best-anti-snoring-mouthpiece', 'best-sleep-socks', 'best-neck-massager-sleep', 'best-sound-machine-tinnitus', 'best-diffuser-sleep', 'best-eye-pillow', 'best-heating-pad-sleep', 'best-bedroom-fan-sleep', 'best-massage-gun-sleep', 'best-under-mattress-sleep-tracker', 'best-sleep-shirt', 'best-cooling-towel-sleep', 'best-sleep-pillow-spray', 'best-acupressure-mat-sleep', 'best-red-light-therapy-sleep', 'best-sleep-balm', 'best-sleep-robe', 'best-bed-fan-sheet', 'best-mouth-tape-sleep', 'best-nasal-dilator-sleep', 'best-sleep-headband', 'best-foam-roller-sleep', 'best-weighted-eye-mask', 'best-grounding-mat-sleep', 'best-bamboo-pajamas-sleep', 'best-sleep-cooling-pad', 'best-oura-ring-alternatives', 'best-sleep-tracker-no-subscription', 'best-smart-alarm-clock', 'best-sleep-mask-travel', 'best-wedge-pillow-acid-reflux', 'best-earplugs-snoring-partner', 'best-cooling-weighted-blanket', 'best-smart-home-sleep-setup', 'best-white-noise-machine-adults', 'best-anti-snoring-chin-strap', 'best-sleep-mask-blackout', 'best-nasal-strips-sleep'],
    'Supplements': ['best-melatonin-supplements', 'best-sleep-supplements-guide', 'best-valerian-root-supplements', 'article-magnesium-sleep', 'sleep-medications-truth', 'best-ashwagandha-sleep', 'best-magnesium-glycinate', 'best-sleep-gummies', 'best-l-theanine-supplement', 'best-melatonin-for-kids', 'best-magnesium-spray-sleep', 'best-sleep-supplement-stack', 'best-sleep-tea', 'best-magnesium-lotion-sleep', 'best-melatonin-patch', 'best-glycine-supplement', 'best-tart-cherry-supplement', 'best-cbd-sleep', 'best-5-htp-supplement-sleep', 'best-passionflower-supplement-sleep', 'best-sleep-supplement-powder', 'best-lemon-balm-supplement-sleep', 'best-pregnenolone-sleep', 'best-magnesium-for-sleep-anxiety', 'best-sleep-supplement-anxiety', 'best-vitamin-d-sleep', 'best-omega-3-sleep', 'best-magnesium-threonate-sleep', 'best-sleep-aids-over-the-counter', 'best-melatonin-gummies-adults', 'best-sleep-supplement-melatonin', 'best-magnesium-glycinate-sleep', 'best-sleep-supplement-women', 'best-sleep-aid-for-anxiety', 'best-deep-sleep-supplement'],
}

CAT_ANCHOR = {
    'Insomnia & CBT-I': 'insomnia-cbti',
    'Sleep Science': 'sleep-science',
    'Caffeine & Nutrition': 'caffeine-nutrition',
    'Sleep Environment': 'sleep-environment',
    'Health Conditions': 'health-conditions',
    'Life Stages': 'life-stages',
    'Timing & Jet Lag': 'timing-jet-lag',
    'Napping & Performance': 'napping-performance',
    'Guides & Plans': 'guides-plans',
    'Mattresses & Bedding': 'mattresses-bedding',
    'Sleep Products': 'sleep-products',
    'Supplements': 'supplements',
}

CAT_META = {
    'Insomnia & CBT-I': ('Evidence-based approaches to insomnia, CBT-I techniques, and sleep disorders.',
        '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>'),
    'Sleep Science': ('Stages, circadian rhythm, dreams, and the biology of rest.',
        '<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>'),
    'Caffeine & Nutrition': ('Caffeine, melatonin, magnesium, alcohol, and food timing.',
        '<path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>'),
    'Sleep Environment': ('Temperature, light, sound — engineering the perfect sleep space.',
        '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>'),
    'Health Conditions': ('Sleep apnea, fibromyalgia, chronic pain, and 200+ conditions A–Z.',
        '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>'),
    'Life Stages': ('Pregnancy, kids, teens, menopause, and seniors.',
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    'Timing & Jet Lag': ('Jet lag, shift work, daylight saving, and schedule resets.',
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
    'Napping & Performance': ('Power naps, sleep inertia, athletic and cognitive output.',
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'),
    'Guides & Plans': ('Step-by-step routines, checklists, challenges, chronotypes.',
        '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'),
    'Mattresses & Bedding': ('Mattresses, pillows, sheets, toppers — buying guides.',
        '<rect x="2" y="9" width="20" height="9" rx="2"/><path d="M4 9V7a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v2"/><line x1="2" y1="18" x2="2" y2="20"/><line x1="22" y1="18" x2="22" y2="20"/>'),
    'Sleep Products': ('Sleep masks, white noise machines, weighted blankets, trackers.',
        '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>'),
    'Supplements': ('Melatonin, magnesium, ashwagandha, L-theanine, CBD.',
        '<path d="M10.5 20.5a7 7 0 0 1-7-7 7 7 0 0 1 7-7l10 10a7 7 0 0 1-10 4z"/><line x1="8.12" y1="8.12" x2="15.88" y2="15.88"/>'),
}

# ---------------------------------------------------------------------------
# Build title map (used for the cross-category search)
# ---------------------------------------------------------------------------
_title_re = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL | re.IGNORECASE)
_strip_suffix = re.compile(r'\s*[|\-–]\s*(SleepWise.*|Sleep.*)$', re.IGNORECASE)

title_map = {}
for fn in os.listdir(POSTS_DIR):
    if not fn.endswith('.html'):
        continue
    slug = fn.replace('.html', '')
    if slug in EXCLUDED:
        continue
    with open(os.path.join(POSTS_DIR, fn), encoding='utf-8') as f:
        html = f.read()
    tm = _title_re.search(html)
    title = re.sub(r'<[^>]+>', '', tm.group(1)).strip() if tm else slug.replace('-', ' ').title()
    title = _strip_suffix.sub('', title).strip()
    title_map[slug] = title

# ---------------------------------------------------------------------------
# Build card HTML + search index
# ---------------------------------------------------------------------------
cards_html = ''
search_index = []
distinct_slugs = set()  # multi-tag: a slug in N categories counts ONCE in the global total

for cat_name, slugs in CATEGORIES.items():
    valid = [s for s in slugs if os.path.exists(os.path.join(POSTS_DIR, s + '.html'))]
    if not valid:
        continue
    slug = CAT_ANCHOR[cat_name]
    desc, icon_path = CAT_META[cat_name]
    distinct_slugs.update(valid)
    cards_html += f'''      <a class="topic-card" href="category/{slug}.html">
        <div class="topic-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon_path}</svg></div>
        <h2>{cat_name} <span class="count">({len(valid)})</span></h2>
        <p class="topic-desc">{desc}</p>
        <span class="browse-link">Browse →</span>
      </a>
'''
    for s in valid:
        search_index.append({
            't': title_map.get(s, s.replace('-', ' ').title()),
            's': s,
            'c': cat_name,
            'cs': slug,
        })

total_count = len(distinct_slugs)  # global total = DISTINCT posts, not sum of category lengths

search_index_json = json.dumps(search_index, ensure_ascii=False, separators=(',', ':'))

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
schema = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "All Sleep Guides & Articles — SleepWise Reviews",
    "description": f"Browse {total_count} sleep guides across 12 topics — insomnia, mattresses, sleep science, health conditions, and more.",
    "url": "https://sleepwisereviews.com/posts/",
    "publisher": {
        "@type": "Organization",
        "name": "SleepWise Reviews",
        "url": "https://sleepwisereviews.com/"
    }
}
schema_block = '<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

# ---------------------------------------------------------------------------
# Article schema (E-E-A-T — Harry Soul author signal)
# Preserve dateModified from existing file so regens are idempotent.
# ---------------------------------------------------------------------------
output_path = os.path.join(POSTS_DIR, 'index.html')
_existing_date_modified = None
if os.path.exists(output_path):
    with open(output_path, encoding='utf-8') as _f:
        _existing_content = _f.read()
    _dm_match = re.search(r'"dateModified":\s*"([^"]+)"', _existing_content)
    if _dm_match:
        _existing_date_modified = _dm_match.group(1)

date_modified = _existing_date_modified or (
    datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + '+00:00'
)

article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": f"All Sleep Guides & Articles — SleepWise Reviews ({total_count} Articles)",
    "description": (
        f"Browse {total_count} science-backed sleep guides across 12 topics — "
        "insomnia, mattresses, sleep science, health conditions, and more."
    ),
    "url": "https://sleepwisereviews.com/posts/",
    "datePublished": "2025-01-01T00:00:00+00:00",
    "dateModified": date_modified,
    "author": {
        "@type": "Person",
        "name": "Harry Soul",
        "url": "https://sleepwisereviews.com/pages/about.html",
        "jobTitle": "Independent Sleep Researcher",
    },
    "publisher": {
        "@type": "Organization",
        "name": "SleepWiseReviews",
        "url": "https://sleepwisereviews.com",
        "logo": {
            "@type": "ImageObject",
            "url": "https://sleepwisereviews.com/favicon.svg",
        },
    },
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://sleepwisereviews.com/posts/",
    },
}
article_schema_block = (
    '<script type="application/ld+json">\n'
    + json.dumps(article_schema, indent=2, ensure_ascii=False)
    + '\n</script>'
)

AUTHOR_BOX = (
    '      <div class="author-box" style="display:flex;align-items:center;gap:1rem;'
    'margin:1rem 0 1.5rem;padding:1rem;background:rgba(26,34,56,0.5);'
    'border:1px solid rgba(201,168,76,0.2);border-radius:8px;font-family:sans-serif;">\n'
    '        <div class="author-avatar" style="font-size:2rem;">\U0001f634</div>\n'
    '        <div class="author-info">\n'
    '          <div class="author-name" style="color:#F0E6C8;font-weight:500;font-size:0.95rem;">'
    'By <a href="../pages/about.html" style="color:#C9A84C;text-decoration:none;">Harry Soul</a>'
    ' - SleepWiseReviews</div>\n'
    '          <div class="author-role" style="color:#7A85A0;font-size:0.82rem;">'
    'Independent Sleep Researcher</div>\n'
    '        </div>\n'
    '      </div>'
)

# ---------------------------------------------------------------------------
# Page HTML
# ---------------------------------------------------------------------------
html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All Sleep Guides &amp; Articles — SleepWise Reviews ({total_count} Articles)</title>
  <meta name="description" content="Browse {total_count} science-backed sleep guides across 12 topics — insomnia, mattresses, sleep science, health conditions, and more." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://sleepwisereviews.com/posts/" />
  <meta property="og:title" content="All Sleep Guides &amp; Articles — SleepWise Reviews" />
  <meta property="og:description" content="Browse {total_count} science-backed sleep guides across 12 topics." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://sleepwisereviews.com/posts/" />
  <meta property="og:image" content="https://sleepwisereviews.com/images/og-default.png" />
  <meta property="og:site_name" content="SleepWise Reviews" />
  {schema_block}
  {article_schema_block}
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0a1628; --card: #111e33; --gold: #c9a84c; --gold-dim: rgba(201,168,76,0.15);
      --text: #e8e0d0; --muted: #8899aa; --border: rgba(201,168,76,0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); font-family: 'Outfit', 'Georgia', sans-serif; line-height: 1.65; }}
    header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 3%; display: flex; align-items: center; justify-content: space-between; }}
    .logo {{ color: var(--gold); text-decoration: none; font-size: 1.3rem; font-weight: 700; }}
    .logo span {{ color: var(--text); }}
    header .home-link {{ color: var(--muted); font-size: 0.9rem; text-decoration: none; }}
    header .home-link:hover {{ color: var(--gold); }}
    main {{ max-width: 1400px; margin: 0 auto; padding: 2.5rem 3% 3rem; }}
    .page-hero {{ margin-bottom: 1rem; }}
    .page-hero a.h1-link {{ text-decoration: none; color: inherit; }}
    h1 {{ font-size: 2.2rem; color: var(--gold); margin-bottom: 0.5rem; line-height: 1.15; }}
    .subtitle {{ color: var(--muted); font-size: 1rem; max-width: 720px; }}
    .search-wrap {{ margin: 1.6rem 0 2.4rem; position: relative; max-width: 720px; }}
    .search-wrap input {{
      width: 100%; padding: 0.85rem 1.2rem 0.85rem 3rem;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; color: var(--text); font-family: inherit; font-size: 1rem;
      outline: none; transition: border-color 0.2s;
    }}
    .search-wrap input:focus {{ border-color: var(--gold); }}
    .search-wrap input::placeholder {{ color: var(--muted); }}
    .search-wrap svg {{ position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); opacity: 0.5; pointer-events: none; }}
    .topic-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 1.4rem; }}
    .topic-card {{
      background: var(--card); border: 1px solid var(--border); border-radius: 14px;
      padding: 1.6rem 1.5rem 1.4rem; display: flex; flex-direction: column;
      text-decoration: none; color: var(--text);
      transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    }}
    .topic-card:hover {{ border-color: var(--gold); transform: translateY(-3px); box-shadow: 0 8px 24px rgba(201,168,76,0.08); }}
    .topic-icon {{
      width: 56px; height: 56px; border-radius: 12px;
      background: var(--gold-dim); color: var(--gold);
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 1rem;
    }}
    .topic-card h2 {{ font-size: 1.1rem; font-weight: 600; color: #f0e6c8; margin-bottom: 0.45rem; line-height: 1.3; }}
    .topic-card .count {{ color: var(--muted); font-size: 0.85rem; font-weight: 400; }}
    .topic-desc {{ color: var(--muted); font-size: 0.9rem; line-height: 1.55; flex: 1; margin-bottom: 1rem; }}
    .browse-link {{ color: var(--gold); font-size: 0.88rem; font-weight: 600; }}

    /* Search results panel */
    .search-results {{ display: none; margin-bottom: 2rem; }}
    .search-results.visible {{ display: block; }}
    .search-group {{ margin-bottom: 1.6rem; }}
    .search-group-header {{
      font-size: 0.78rem; font-weight: 600; color: var(--gold); text-transform: uppercase; letter-spacing: 0.06em;
      margin-bottom: 0.6rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border);
    }}
    .search-group-header a {{ color: inherit; text-decoration: none; }}
    .search-result {{
      display: block; background: var(--card); border: 1px solid var(--border); border-radius: 10px;
      padding: 0.85rem 1.1rem; margin-bottom: 0.5rem; text-decoration: none; color: var(--text);
      transition: border-color 0.15s;
    }}
    .search-result:hover {{ border-color: var(--gold); }}
    .search-result-title {{ font-size: 0.95rem; color: #f0e6c8; line-height: 1.4; }}
    .no-results {{ display: none; }}
    .no-results-panel {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.6rem 1.8rem; }}
    .no-results-panel h3 {{ color: var(--gold); font-size: 1rem; margin-bottom: 0.5rem; }}
    .no-results-panel p {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 1.2rem; }}
    .contact-options {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    .contact-btn {{
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem;
      font-family: inherit; text-decoration: none; font-weight: 600;
      border: 1px solid var(--border); color: var(--text); background: rgba(255,255,255,0.04);
      transition: border-color 0.2s, color 0.2s;
    }}
    .contact-btn:hover {{ border-color: var(--gold); color: var(--gold); }}
    .contact-btn.gold {{ background: var(--gold); color: #07101f; border-color: var(--gold); }}
    .contact-btn.gold:hover {{ background: #e8c96a; }}

    footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 3rem; }}
    footer a {{ color: var(--gold); text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
    @media (max-width: 700px) {{
      h1 {{ font-size: 1.6rem; }}
      .topic-grid {{ grid-template-columns: 1fr; gap: 1rem; }}
      main {{ padding: 1.8rem 4% 2rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <a class="logo" href="../">SleepWise<span>Reviews</span></a>
    <a class="home-link" href="../">← Home</a>
  </header>
  <main>
    <div class="page-hero">
      <a class="h1-link" href="./" aria-label="All Sleep Guides and Articles — back to topics"><h1>All Sleep Guides &amp; Articles</h1></a>
{AUTHOR_BOX}
      <p class="subtitle">{total_count} science-backed articles across 12 topics. Pick a topic below, or search across everything.</p>
    </div>
    <div class="search-wrap">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      <input type="text" id="search" placeholder="Search {total_count} articles — try 'mattress', 'melatonin', 'back pain'..." autocomplete="off" />
    </div>
    <div class="search-results" id="search-results"></div>
    <div class="no-results" id="no-results">
      <div class="no-results-panel">
        <h3>No articles match your search</h3>
        <p>Try a different keyword, or let us help you find what you need:</p>
        <div class="contact-options">
          <a href="mailto:hello@sleepwisereviews.com" class="contact-btn">&#x2709; Email Us</a>
          <a href="https://www.instagram.com/sleepwisereviews/" class="contact-btn" rel="noopener noreferrer" target="_blank">&#x1F4F7; Instagram DM</a>
          <a href="https://sleepwisereviews.com/subscribe.html" class="contact-btn gold">&#x1F4E7; Weekly Sleep Tips</a>
        </div>
      </div>
    </div>
    <div class="topic-grid" id="topic-grid">
{cards_html}    </div>
  </main>
  <footer>
    <p>&copy; 2025-2026 <a href="../">SleepWise Reviews</a> · Evidence-based sleep guidance</p>
  </footer>
  <script>
    (function() {{
      var INDEX = {search_index_json};
      var input = document.getElementById('search');
      var grid = document.getElementById('topic-grid');
      var resultsBox = document.getElementById('search-results');
      var noResults = document.getElementById('no-results');

      function clearChildren(node) {{
        while (node.firstChild) node.removeChild(node.firstChild);
      }}

      function makeEl(tag, opts) {{
        var el = document.createElement(tag);
        if (opts) {{
          if (opts.cls) el.className = opts.cls;
          if (opts.text) el.textContent = opts.text;
          if (opts.href) el.setAttribute('href', opts.href);
          if (opts.aria) el.setAttribute('aria-label', opts.aria);
        }}
        return el;
      }}

      function renderResults(matches) {{
        clearChildren(resultsBox);
        var groups = {{}};
        var order = [];
        matches.forEach(function(m) {{
          if (!groups[m.c]) {{ groups[m.c] = {{ cs: m.cs, items: [] }}; order.push(m.c); }}
          groups[m.c].items.push(m);
        }});
        order.forEach(function(cn) {{
          var g = groups[cn];
          var groupEl = makeEl('div', {{ cls: 'search-group' }});
          var headerEl = makeEl('div', {{ cls: 'search-group-header' }});
          var headerLink = makeEl('a', {{ href: 'category/' + g.cs + '.html', text: cn + ' (' + g.items.length + ')' }});
          headerEl.appendChild(headerLink);
          groupEl.appendChild(headerEl);
          g.items.forEach(function(it) {{
            var card = makeEl('a', {{ cls: 'search-result', href: it.s + '.html' }});
            var titleEl = makeEl('div', {{ cls: 'search-result-title', text: it.t }});
            card.appendChild(titleEl);
            groupEl.appendChild(card);
          }});
          resultsBox.appendChild(groupEl);
        }});
      }}

      input.addEventListener('input', function() {{
        var q = this.value.toLowerCase().trim();
        if (!q) {{
          resultsBox.classList.remove('visible');
          clearChildren(resultsBox);
          grid.style.display = '';
          noResults.style.display = 'none';
          return;
        }}
        var matches = INDEX.filter(function(it) {{ return it.t.toLowerCase().indexOf(q) !== -1; }});
        grid.style.display = 'none';
        if (matches.length === 0) {{
          resultsBox.classList.remove('visible');
          clearChildren(resultsBox);
          noResults.style.display = 'block';
          return;
        }}
        noResults.style.display = 'none';
        renderResults(matches);
        resultsBox.classList.add('visible');
      }});
    }})();
  </script>
</body>
</html>
'''

output_path = os.path.join(POSTS_DIR, 'index.html')
with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html_out)

print(f'Generated posts/index.html ({total_count} posts, {len(CATEGORIES)} categories)')
