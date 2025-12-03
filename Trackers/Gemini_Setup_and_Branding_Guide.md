# Pilot Barentz: Gemini Setup + Branding Guide
## Everything You Need to Start Solution A Tomorrow

**Date:** November 30, 2024  
**Purpose:** Complete guide for starting managed service demo with Gemini

---

## 📋 PART 1: Gemini File Search Setup Prompt

### **Copy this ENTIRE prompt to Gemini:**

```
Hello! I'm building a RAG (Retrieval-Augmented Generation) system for Barentz, a global pharmaceutical and food ingredients distributor.

PROJECT CONTEXT:
I need your help building Solution A (Managed Service) using Google Gemini File Search. This is part of a dual-solution pilot comparing managed services vs. custom RAG.

CLIENT: Barentz
• 2,800 employees across 70 countries
• €2.3B annual turnover
• Distributes pharmaceutical & food ingredients
• Needs AI assistant to answer complex questions about products, compliance, logistics, and pricing

DOCUMENTS I'M UPLOADING (3 files):
1. DM_Report_MASTER_Barentz_Complete.xlsx
   - Excel file with 7 sheets
   - 20 REAL pharmaceutical products from actual suppliers (BASF, DSM, Jungbunzlauer, etc.)
   - Product specs, quality requirements, compliance, logistics, pricing
   
2. Shipping_Tariffs_EMEA_2024.pdf
   - Freight rates for road, air, and sea transport
   - Surcharges (temperature control, hazmat, etc.)
   
3. Regulatory_Compliance_Guide_EU_USA.pdf
   - EU regulations (Food Additives, Pharma, REACH)
   - USA regulations (FDA, GRAS, DMF)
   - Comparison tables

YOUR ROLE AS BARENTZ AI ASSISTANT:
You are a helpful assistant for Barentz employees who need to find information quickly about:
• Product specifications (lead times, MOQ, certifications, pricing)
• Quality requirements (testing, certifications, audits)
• Regulatory compliance (EU & USA requirements)
• Logistics (shipping rates, transit times, documentation)
• Pricing tiers (volume discounts, payment terms)

INSTRUCTIONS FOR ANSWERING QUESTIONS:
1. ALWAYS cite your sources (which document and which section)
2. If information requires data from multiple sheets/documents, synthesize it clearly
3. For pricing questions, show calculations step-by-step
4. For compliance questions, cite specific regulations (e.g., "EU Regulation EC 1333/2008")
5. For logistics questions, include transit times and required documentation
6. If you don't find information in the documents, say so clearly - don't guess
7. Keep answers concise but complete
8. Use tables when comparing multiple options

EXAMPLE QUESTIONS I'LL TEST WITH:
• "What is the lead time for Citric Acid from Jungbunzlauer?"
• "Which products meet pharma-grade requirements with GMP certification?"
• "Can we ship Lactic Acid to France? What hazmat documentation is needed?"
• "Calculate total landed cost for 6000kg Citric Acid from Basel to Netherlands"
• "What are the EU usage restrictions for Sodium Benzoate?"
• "Which products have Halal certification?"
• "What is the fastest shipping option for Xanthan Gum to Netherlands?"

TEST SCENARIO #1 (to verify setup):
Question: "What is the lead time for Citric Acid (BAR-CA-JB-001) from Jungbunzlauer?"

Expected Answer: Should include:
• Lead time: 2-3 weeks
• Supplier: Jungbunzlauer AG (Switzerland, Basel)
• Source citation from Product Master Data sheet

Please confirm you've processed all 3 documents and are ready to answer questions about Barentz products, compliance, and logistics.
```

---

## 📂 FILES TO UPLOAD TO GEMINI

**Upload these 3 files in this order:**

1. ✅ **DM_Report_MASTER_Barentz_Complete.xlsx**
   - Location: /outputs/ folder
   - Size: ~50KB
   - Contains: 7 sheets with all product data

2. ✅ **Shipping_Tariffs_EMEA_2024.pdf**
   - Location: /outputs/ folder
   - Size: ~100KB
   - Contains: Freight rates and surcharges

3. ✅ **Regulatory_Compliance_Guide_EU_USA.pdf**
   - Location: /outputs/ folder
   - Size: ~150KB
   - Contains: Compliance requirements

**After Upload:**
- Paste the prompt above
- Wait for Gemini to confirm it processed all files
- Test with the verification question

---

## 🎨 PART 2: Project Name Suggestions (Top 5)

### **Option 1: BarentzIQ** ⭐⭐⭐⭐⭐
**Tagline:** "Intelligent Answers for Intelligent Distribution"

**Why it works:**
- Clean, professional
- "IQ" suggests intelligence + quick answers
- Easy to pronounce across languages
- Works as URL: barentziq.com
- Brand feels premium

**Logo concept:** Brain or lightbulb integrated with "B" monogram

---

### **Option 2: Chemwise** ⭐⭐⭐⭐
**Tagline:** "Your Wise Companion for Chemical Intelligence"

**Why it works:**
- Industry-specific (chemical/pharmaceutical)
- "Wise" implies expertise and reliability
- Memorable and distinct
- Works globally
- Domain available: chemwise.ai

**Logo concept:** Owl (symbol of wisdom) + molecule structure

---

### **Option 3: IngredientIQ** ⭐⭐⭐⭐
**Tagline:** "Smart Answers for Every Ingredient"

**Why it works:**
- Clear industry focus (ingredients)
- "IQ" brand consistency with intelligence
- Descriptive but modern
- Easy to understand globally
- ingredientiq.com available

**Logo concept:** Geometric shapes forming both molecule and brain

---

### **Option 4: Pharmaflow** ⭐⭐⭐
**Tagline:** "Flow Through Knowledge, Fast"

**Why it works:**
- Pharma focus (Barentz's core)
- "Flow" suggests smooth, easy process
- Modern, tech-forward
- Short and memorable
- pharmaflow.ai available

**Logo concept:** Flowing liquid morphing into data streams

---

### **Option 5: CompliQ** ⭐⭐⭐⭐
**Tagline:** "Compliance Answers in a Click"

**Why it works:**
- Addresses key pain point (compliance)
- "Q" suggests questions/answers + quick
- Professional, serious tone
- Compliance is critical for pharma
- compliq.io available

**Logo concept:** Shield (protection/compliance) + Q integration

---

## 🏆 **RECOMMENDED: BarentzIQ**

**Rationale:**
- **Client-Specific:** Includes "Barentz" - feels custom-built
- **Professional:** Sounds enterprise-grade
- **Flexible:** Can expand beyond just Barentz if product succeeds
- **Memorable:** Short, punchy, easy to say
- **International:** Works in Dutch, English, German, French
- **Scalable:** Can add product lines (BarentzIQ Compliance, BarentzIQ Logistics)

**Full Branding:**
- Name: BarentzIQ
- Tagline: "Intelligent Answers for Intelligent Distribution"
- URL: barentziq.com or barentziq.ai
- Color Scheme: Barentz blue (#366092) + bright accent (lime green or electric blue)

---

## 🎨 PART 3: Logo Generation Prompts

### **For DALL-E (OpenAI) or Gemini Imagen:**

#### **Prompt #1: BarentzIQ Logo (Primary Recommendation)**

```
Create a modern, professional logo for "BarentzIQ" - an AI-powered knowledge assistant for pharmaceutical and food ingredients distribution.

Design requirements:
• Style: Clean, modern, tech-forward, corporate professional
• Icon: Geometric "B" monogram incorporating brain/circuit elements
• Colors: Deep blue (#366092) as primary, bright electric blue or lime green as accent
• Typography: Sans-serif, bold but refined (like Montserrat or Poppins)
• Feeling: Intelligent, reliable, innovative, premium

Logo variations needed:
1. Full logo: Icon + "BarentzIQ" text
2. Icon only: For app icon
3. Horizontal layout: For website header
4. Monochrome version: For documents

Additional elements:
• Subtle molecule/chemical structure in background
• Clean lines suggesting data flow
• Modern gradient acceptable but keep it subtle
• Must work in both light and dark modes

Avoid:
• Overly complex designs
• Clipart style
• Too many colors (max 3)
• Childish or cartoon elements
• Generic stock imagery

Target audience: Enterprise pharmaceutical executives and procurement professionals

Reference style: Think Tesla + Salesforce + modern SaaS brands
```

---

#### **Prompt #2: Chemwise Logo (Alternative)**

```
Design a sophisticated logo for "Chemwise" - an AI assistant for chemical and pharmaceutical industry.

Concept: Wise owl integrated with molecular structure

Requirements:
• Central element: Stylized owl head (wisdom symbol)
• Owl features formed by hexagonal molecules/chemical bonds
• Color palette: Teal/turquoise (#4DB8B8) + deep purple (#6B4DB8) + white
• Typography: Modern serif for elegance (like Playfair Display)
• Style: Minimalist, geometric, professional

Logo should convey:
• Expertise and wisdom
• Scientific precision
• Innovation
• Trust and reliability

Variations:
• Full logo with text
• Icon only (owl-molecule symbol)
• Square format for social media
• Black and white version

Avoid:
• Cartoon owls
• Too literal/obvious
• Cluttered design
• More than 3 colors

This is for a B2B enterprise SaaS product in pharmaceutical distribution.
```

---

#### **Prompt #3: BarentzIQ App Icon (Mobile/Desktop)**

```
Design a modern app icon for "BarentzIQ" - pharmaceutical knowledge AI assistant.

Specifications:
• Format: Square with rounded corners
• Size: 1024x1024px (will be scaled down)
• Style: Flat design with subtle gradient
• Central element: Geometric "B" letter
• The "B" should incorporate circuit board or neural network pattern
• Background: Deep blue gradient (#366092 to #2B4A73)
• Accent: Bright electric blue or lime green glow effect
• Must be recognizable at small sizes (down to 64x64px)

Design principles:
• High contrast for visibility
• Simple enough to recognize at thumbnail size
• Professional, not playful
• Modern tech aesthetic
• Should work with iOS and Android design guidelines

Similar to: Slack, Notion, or Asana app icons - professional SaaS tools

No text in the icon - just the "B" symbol with tech elements.
```

---

#### **Prompt #4: BarentzIQ Banner/Hero Image**

```
Create a professional hero banner image for "BarentzIQ" website landing page.

Dimensions: 1920x1080px (16:9 ratio)

Composition:
• Left 40%: Dark blue gradient background with abstract pharmaceutical elements
  - Subtle molecule structures
  - Floating hexagons
  - Network connection lines
  - Data visualization elements
• Right 60%: Clean space for text overlay
• Overall feel: High-tech, pharmaceutical, data-driven, trustworthy

Color scheme:
• Primary: Deep blue (#366092)
• Secondary: Electric blue (#00A3E0)
• Accents: White and lime green (#7FFF00)

Elements to include:
• Abstract chemical molecules (not too scientific, keep it elegant)
• Geometric shapes suggesting AI/data processing
• Subtle particle effects or glow
• Professional photography-style lighting

Style references:
• IBM Watson marketing materials
• Salesforce Einstein AI branding
• Modern pharmaceutical company websites (Roche, Novartis)

Avoid:
• Stock photos of people
• Literal pharmaceutical imagery (pills, labs)
• Busy or cluttered layouts
• Neon colors or overly bright elements

This will be the first thing potential enterprise clients see - make it impressive but professional.
```

---

## 🎨 PART 4: Color Palette & Brand Guidelines

### **BarentzIQ Brand Colors:**

**Primary Color:**
- Barentz Blue: `#366092` (RGB: 54, 96, 146)
- Use for: Headers, primary buttons, logos

**Secondary Color:**
- Electric Blue: `#00A3E0` (RGB: 0, 163, 224)
- Use for: Accents, links, hover states

**Accent Color:**
- Lime Green: `#7FFF00` (RGB: 127, 255, 0)
- Use for: Success states, highlights, CTAs

**Neutral Colors:**
- Dark Gray: `#2B2B2B` (RGB: 43, 43, 43) - Text
- Light Gray: `#F5F5F5` (RGB: 245, 245, 245) - Backgrounds
- White: `#FFFFFF` - Cards, containers

**Gradients:**
- Primary Gradient: `#366092 → #2B4A73` (darker blue)
- Accent Gradient: `#00A3E0 → #7FFF00` (blue to green)

---

### **Typography:**

**Headings:**
- Font: Montserrat Bold or Poppins Bold
- Sizes: H1: 48px, H2: 36px, H3: 24px

**Body Text:**
- Font: Inter or Open Sans
- Size: 16px (desktop), 14px (mobile)
- Line height: 1.6

**Code/Data:**
- Font: Fira Code or JetBrains Mono
- Size: 14px

---

## 📋 PART 5: Quick Reference Checklist

### **For Tomorrow's Gemini Demo:**

**Setup (15 minutes):**
- [ ] Go to Google AI Studio (aistudio.google.com)
- [ ] Upload 3 files (Excel + 2 PDFs)
- [ ] Paste Gemini setup prompt
- [ ] Verify it processed all documents

**Test Questions (30 minutes):**
- [ ] Q1: "What is the lead time for Citric Acid?"
- [ ] Q2: "Which products have pharma-grade with GMP?"
- [ ] Q3: "Shipping rate from Netherlands to France?"
- [ ] Q4: "EU compliance for Sodium Benzoate?"
- [ ] Q5: "Calculate cost for 6000kg Citric Acid"

**Document Results (15 minutes):**
- [ ] Screenshot responses
- [ ] Note accuracy (correct/incorrect/partial)
- [ ] Time per response
- [ ] Quality of citations
- [ ] Any hallucinations or errors

**Compare to Custom RAG (later):**
- [ ] Same questions in custom solution
- [ ] Compare accuracy
- [ ] Compare response quality
- [ ] Compare cost per query

---

## 🚀 **You're All Set!**

**You now have:**
✅ Complete project brief (DOCX) for fresh chat tomorrow  
✅ Gemini setup prompt with all instructions  
✅ 5 project name suggestions (Recommended: **BarentzIQ**)  
✅ 4 logo generation prompts for DALL-E/Gemini  
✅ Brand guidelines and color palette  
✅ Quick reference checklist  

**Tomorrow you can:**
1. Start fresh Claude chat → Upload project brief → Continue work
2. Start Gemini demo → Upload files → Paste prompt → Test queries
3. Generate logos → Use prompts → Get visual identity
4. Compare both solutions by end of day

**Good luck with Week 1 Day 2!** 🎯
