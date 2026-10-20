CROP_DISPLAY = {
    "Wheat": {"en": "Wheat", "hi": "गेहूं", "mr": "गहू"},
    "Jowar": {"en": "Jowar", "hi": "ज्वार", "mr": "ज्वारी"},
    "Sugarcane": {"en": "Sugarcane", "hi": "गन्ना", "mr": "ऊस"},
    "Cotton": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
    "Groundnut": {"en": "Groundnut", "hi": "मूंगफली", "mr": "शेंगदाणा"},
}

NUTRIENT_DISPLAY = {
    "Nitrogen": {"en": "Nitrogen", "hi": "नाइट्रोजन", "mr": "नायट्रोजन"},
    "Phosphorus": {"en": "Phosphorus", "hi": "फॉस्फोरस", "mr": "फॉस्फरस"},
    "Potassium": {"en": "Potassium", "hi": "पोटैशियम", "mr": "पोटॅशियम"},
    "pH": {"en": "pH", "hi": "pH", "mr": "pH"},
}

STATUS_DISPLAY = {
    "Low": {"en": "Low", "hi": "कम", "mr": "कमी"},
    "High": {"en": "High", "hi": "अधिक", "mr": "जास्त"},
    "Optimal": {"en": "Optimal", "hi": "उपयुक्त", "mr": "योग्य"},
}

_MESSAGES = {
    "en": {
        "GREETING": (
            "Hello! I'm the Smart Agri assistant. "
            "I can help you understand your crop recommendation, "
            "soil analysis, fertilizer recommendation, and yield prediction."
        ),
        "HELP": (
            "I can help you with:\n"
            "• Crop recommendations\n"
            "• Crop recommendation probabilities\n"
            "• Soil nutrient status\n"
            "• Fertilizer recommendations\n"
            "• Fertilizer dosage and application\n"
            "• Yield prediction and interpretation\n\n"
            "You can also ask about a specific crop by name, e.g. "
            "\"what fertilizer for Jowar\" — even if it's not your "
            "current top recommendation."
        ),
        "SYSTEM_OVERVIEW": (
            "Smart Agri is a decision-support system that analyzes "
            "your soil and environmental inputs to recommend suitable "
            "crops, identify soil nutrient gaps, suggest fertilizers, "
            "and predict yield."
        ),
        "HOW_TO_USE": (
            "To use Smart Agri:\n"
            "1. Set Nitrogen, Phosphorus, Potassium, pH, temperature, and rainfall.\n"
            "2. Choose a target crop for fertilizer and yield.\n"
            "3. Click Run Analysis.\n"
            "4. Review crop, soil, fertilizer, and yield results on the dashboard.\n"
            "5. Ask me follow-up questions in English, Hindi, or Marathi."
        ),
        "DASHBOARD": (
            "The dashboard shows your analysis in one page: crop ranking, "
            "soil nutrient status versus the crop ideal, fertilizer advice, "
            "and predicted yield charts. Run an analysis first, then scroll "
            "to each section or ask me about a specific result."
        ),
        "ML_MODEL_EXPLANATION": (
            "Smart Agri uses a Random Forest classifier for crop recommendation "
            "and a Random Forest regressor for yield prediction. Soil gaps and "
            "fertilizer advice are rule-based using ideal nutrient ranges for "
            "each supported crop."
        ),
        "SUPPORTED_CROPS": "Smart Agri currently supports soil adjustment and fertilizer recommendations for: {crops}.",
        "SUPPORTED_CROPS_EMPTY": "I don't have the list of supported crops available right now. Please check the Smart Agri dashboard.",
        "CROP_RECOMMENDATION": "Based on your current soil and environmental inputs, Smart Agri recommends {crop} as the top crop.",
        "CROP_RECOMMENDATION_EXPLANATION": (
            "{crop} was recommended because it received the highest prediction probability of {probability:.1f}% among the crops considered by the crop model."
        ),
        "CROP_RECOMMENDATION_EXPLANATION_NO_PROBS": (
            "{crop} was recommended as the best fit based on your soil and environmental inputs, but I don't have the detailed probability breakdown right now."
        ),
        "CROP_PROBABILITY_HEADER": "Here are the top crop predictions:",
        "CROP_PROBABILITY_EMPTY": "I don't have the crop probability breakdown available for this report.",
        "CROP_PROBABILITY_LINE": "• {crop}: {probability:.1f}%",
        "CROP_SOIL_UNSUPPORTED": "Smart Agri doesn't have soil compatibility data for {crop}. Supported crops are: {supported}.",
        "CROP_SOIL_MATCH": "{prefix}Your soil is a good match for {crop} — all measured nutrients are within the optimal range.",
        "CROP_SOIL_MISMATCH": "{prefix}Your soil has some mismatches for {crop}:\n{lines}",
        "CROP_MISMATCH_BETTER": (
            "There may be a mismatch — for your soil inputs, {top_crop} scored higher "
            "than {crop}, the crop you have selected. You can switch the target crop "
            "dropdown to {top_crop} to see its fertilizer and yield guidance."
        ),
        "CROP_MISMATCH_BEST": "{crop} is currently the best-matching crop for your soil and climate inputs.",
        "SOIL_MISMATCH_LINE": "• {nutrient} is {status} (current: {current}, ideal: {ideal})",
        "SOIL_ANALYSIS": (
            "Soil analysis versus ideal ranges for your target crop {crop} "
            "(N, P, K in kg/ha; pH is unitless). Status uses ±tolerance around "
            "the crop mean (N ±10, P ±5, K ±5, pH ±0.3):\n"
            "{lines}"
        ),
        "SOIL_ANALYSIS_LINE": "• {nutrient}: {current}{unit} — {status} (ideal {ideal}{unit})",
        "SOIL_IMBALANCE_HEADER": (
            "{count} imbalance(s) versus the target crop {crop}:"
        ),
        "SOIL_IMBALANCE_LINE": (
            "• {nutrient}: {current}{unit} is {status} (ideal {ideal}{unit}). {action}"
        ),
        "SOIL_ALL_OPTIMAL": (
            "All measured nutrients are within the documented tolerance of the "
            "ideal range for {crop}. That is a match to the model's thresholds, "
            "not a guarantee of field performance."
        ),
        "SOIL_ACTION_LOW": "Consider supplying this nutrient (see the fertilizer plan for {crop}).",
        "SOIL_ACTION_HIGH": "Avoid adding more of this nutrient this season.",
        "SOIL_ACTION_OK": "No correction needed for this parameter.",
        "YIELD_UNAVAILABLE": (
            "There is no stored yield estimate for {crop} in this analysis. "
            "I will not invent a number. Supported crops are: {crops}."
        ),
        "YIELD_PREDICTION_BOTH": (
            "These are model estimates, not guaranteed harvests.\n"
            "• Target crop {target}: {target_yield:,.1f} kg/ha\n"
            "• Recommended crop {recommended}: {recommended_yield:,.1f} kg/ha"
        ),
        "YIELD_ESTIMATE_NOTE": " This is a model estimate in kg/ha, not a guaranteed harvest.",
        "FERTILIZER_OTHER_CROP": (
            "The fertilizer plan in this analysis is for the target crop {target}, "
            "not for {crop}. Set {crop} as the target crop and run analysis again "
            "to get its fertilizer guidance."
        ),
        "GROWN_CROP_NONE": "No actual grown crop has been recorded for this analysis yet.",
        "GROWN_CROP_IS": "The actual grown crop recorded for this run is {crop}.",
        "NUTRIENT_NO_ADJUSTMENT": (
            "Your {nutrient} level is {value}{unit}. However, Smart Agri does not currently have soil adjustment data for {crop}, so I cannot determine whether this value is Low, High, or Optimal for that crop."
        ),
        "NUTRIENT_STATUS": (
            "{prefix}Your {nutrient} level is {current}{unit}. For {crop}, the ideal value used by Smart Agri is {ideal}{unit}. Your status is {status}."
        ),
        "SOIL_STATUS_EXPLANATION": (
            "Smart Agri uses three soil status categories:\n"
            "• Low — the current value is below the ideal range.\n"
            "• High — the current value is above the ideal range.\n"
            "• Optimal — the value is within the defined tolerance range."
        ),
        "FERTILIZER_UNSUPPORTED": (
            "Smart Agri does not currently have fertilizer recommendations for {crop}. The fertilizer recommendation module currently supports: {supported}."
        ),
        "FERTILIZER_BALANCED": "{prefix}Your soil is well-balanced for {crop}. No nutrient correction is currently needed.",
        "FERTILIZER_BASED": "{prefix}Based on your soil analysis:",
        "FERTILIZER_CONDITION_LINE": "• {nutrient} is {status} → {label}",
        "FERTILIZER_PRIMARY": "\nPrimary fertilizer for {crop}: {fertilizer}",
        "FERTILIZER_DOSAGE_UNSUPPORTED": "Smart Agri does not currently have fertilizer dosage data for {crop}.",
        "FERTILIZER_DOSAGE_NONE": "{prefix}No specific fertilizer dosage is currently required for {crop} because your soil is within the optimal range.",
        "FERTILIZER_DOSAGE_HEADER": "{prefix}Recommended fertilizer application:",
        "FERTILIZER_DOSAGE_LINE": "• {label}: {dose}",
        "WHY_FERT_UNSUPPORTED": "Smart Agri does not currently have fertilizer data for {crop}.",
        "WHY_FERT_NONE": "{prefix}No corrective fertilizer is currently required for {crop} because your soil values are within the optimal range.",
        "WHY_FERT_HEADER": "{prefix}Here's why each recommendation applies:",
        "WHY_FERT_LINE": "• {label}: {reason}",
        "FERT_EXPLAIN_NONE": "{prefix}There are currently no corrective fertilizer recommendations for {crop}.",
        "FERT_EXPLAIN_HEADER": "{prefix}Your fertilizer recommendations are:",
        "FERT_EXPLAIN_LOW": "• {label} ({npk}) — {reason}",
        "FERT_EXPLAIN_HIGH": "• {label} — {reason}",
        "FERT_EXPLAIN_LINE": "• {label} ({npk}) — {reason}",
        "YIELD_NONE": "Smart Agri does not currently have a yield prediction for {crop}.",
        "YIELD_PREDICTION": (
            "{prefix}Estimated yield for {crop} is {yield_kg:,.1f} kg/ha. "
            "This is a model estimate, not a guaranteed harvest."
        ),
        "YIELD_INTERP_NONE": "Smart Agri does not currently have a yield interpretation for {crop}.",
        "YIELD_LOW": "Low yield — soil needs significant correction.",
        "YIELD_MOD": "Moderate yield — improvement is possible.",
        "YIELD_GOOD": "Good yield — conditions are favorable.",
        "YIELD_HIGH": "High yield — excellent conditions (typical for sugarcane).",
        "YIELD_FACTORS": (
            "The Smart Agri yield prediction uses the available soil and environmental inputs from your analysis, including Nitrogen, Phosphorus, Potassium, temperature, rainfall, pH, and the selected crop."
        ),
        "YIELD_STATUS_EXPLANATION": (
            "Smart Agri interprets predicted yield using categories such as Moderate, Good, and High. These indicate the model's interpretation of the predicted yield for the selected crop."
        ),
        "OUT_OF_SCOPE": (
            "I'm designed specifically for Smart Agri. I can answer questions about the software, your soil analysis, crop recommendations, fertilizer recommendations, and yield prediction."
        ),
        "UNKNOWN": "I'm not sure what you're asking. Try asking about your crop recommendation, soil, fertilizer, or yield prediction.",
        "FALLBACK": "I don't have an answer for that yet. Please ask something related to Smart Agri.",
        "OVERRIDE_PREFIX": "(Note: your current report's top recommendation is {chosen}, but here's the analysis for {crop} specifically.)\n\n",
    },
    "hi": {
        "GREETING": (
            "नमस्ते! मैं स्मार्ट एग्री सहायक हूँ। "
            "मैं आपकी फसल सिफारिश, मिट्टी विश्लेषण, खाद सिफारिश और उपज अनुमान समझने में मदद कर सकता हूँ।"
        ),
        "HELP": (
            "मैं इनमें मदद कर सकता हूँ:\n"
            "• फसल सिफारिश\n"
            "• फसल संभावना प्रतिशत\n"
            "• मिट्टी पोषक तत्व स्थिति\n"
            "• खाद सिफारिश\n"
            "• खाद की मात्रा और उपयोग\n"
            "• उपज अनुमान और अर्थ\n\n"
            "आप किसी फसल का नाम भी पूछ सकते हैं, जैसे "
            "\"ज्वार के लिए कौन सी खाद\" — भले वह सबसे ऊपर की सिफारिश न हो।"
        ),
        "SYSTEM_OVERVIEW": (
            "स्मार्ट एग्री एक निर्णय-सहायता प्रणाली है। यह आपकी मिट्टी और मौसम संबंधी जानकारी से उपयुक्त फसल सुझाती है, पोषक अंतर बताती है, खाद सुझाती है और उपज का अनुमान लगाती है।"
        ),
        "HOW_TO_USE": (
            "स्मार्ट एग्री का उपयोग:\n"
            "1. नाइट्रोजन, फॉस्फोरस, पोटैशियम, pH, तापमान और वर्षा सेट करें।\n"
            "2. खाद और उपज के लिए लक्ष्य फसल चुनें।\n"
            "3. विश्लेषण चलाएँ पर क्लिक करें।\n"
            "4. डैशबोर्ड पर फसल, मिट्टी, खाद और उपज देखें।\n"
            "5. अंग्रेज़ी, हिंदी या मराठी में मुझसे प्रश्न पूछें।"
        ),
        "DASHBOARD": (
            "डैशबोर्ड एक ही पृष्ठ पर विश्लेषण दिखाता है: फसल रैंकिंग, फसल के आदर्श की तुलना में मिट्टी, खाद सलाह और उपज चार्ट। पहले विश्लेषण चलाएँ, फिर खंड देखें या मुझसे किसी परिणाम के बारे में पूछें।"
        ),
        "ML_MODEL_EXPLANATION": (
            "स्मार्ट एग्री फसल सिफारिश के लिए रैंडम फॉरेस्ट वर्गीकरण मॉडल और उपज के लिए रैंडम फॉरेस्ट रिग्रेशन मॉडल उपयोग करता है। मिट्टी का अंतर और खाद सलाह प्रत्येक फसल की आदर्श पोषक सीमाओं पर आधारित नियम हैं।"
        ),
        "SUPPORTED_CROPS": "स्मार्ट एग्री अभी इन फसलों के लिए मिट्टी समायोजन और खाद सिफारिश देता है: {crops}।",
        "SUPPORTED_CROPS_EMPTY": "अभी समर्थित फसलों की सूची उपलब्ध नहीं है। कृपया स्मार्ट एग्री डैशबोर्ड देखें।",
        "CROP_RECOMMENDATION": "आपकी वर्तमान मिट्टी और पर्यावरण जानकारी के आधार पर, स्मार्ट एग्री सबसे उपयुक्त फसल {crop} सुझाता है।",
        "CROP_RECOMMENDATION_EXPLANATION": (
            "{crop} इसलिए सुझाई गई क्योंकि फसल मॉडल में इसकी संभावना सबसे अधिक {probability:.1f}% रही।"
        ),
        "CROP_RECOMMENDATION_EXPLANATION_NO_PROBS": (
            "{crop} आपकी मिट्टी और पर्यावरण जानकारी के अनुसार सबसे उपयुक्त मानी गई, लेकिन विस्तृत संभावना सूची अभी उपलब्ध नहीं है।"
        ),
        "CROP_PROBABILITY_HEADER": "शीर्ष फसल अनुमान ये हैं:",
        "CROP_PROBABILITY_EMPTY": "इस रिपोर्ट के लिए फसल संभावना विवरण उपलब्ध नहीं है।",
        "CROP_PROBABILITY_LINE": "• {crop}: {probability:.1f}%",
        "CROP_SOIL_UNSUPPORTED": "स्मार्ट एग्री के पास {crop} के लिए मिट्टी अनुकूलता डेटा नहीं है। समर्थित फसलें: {supported}।",
        "CROP_SOIL_MATCH": "{prefix}आपकी मिट्टी {crop} के लिए अच्छी मेल खाती है — सभी मापे गए पोषक तत्व उपयुक्त सीमा में हैं।",
        "CROP_SOIL_MISMATCH": "{prefix}{crop} के लिए आपकी मिट्टी में कुछ अंतर हैं:\n{lines}",
        "CROP_MISMATCH_BETTER": (
            "थोड़ा बेमेल हो सकता है — आपकी मिट्टी के लिए, {top_crop} ने आपकी चुनी हुई फसल "
            "{crop} से अधिक स्कोर किया। {top_crop} की खाद और उपज जानकारी देखने के लिए "
            "लक्ष्य फसल सूची में इसे चुनें।"
        ),
        "CROP_MISMATCH_BEST": "आपकी मिट्टी और मौसम जानकारी के लिए {crop} अभी सबसे उपयुक्त फसल है।",
        "SOIL_MISMATCH_LINE": "• {nutrient} {status} है (वर्तमान: {current}, आदर्श: {ideal})",
        "SOIL_ANALYSIS": (
            "लक्ष्य फसल {crop} की आदर्श सीमा के मुकाबले मिट्टी विश्लेषण "
            "(N, P, K kg/ha में; pH इकाईहीन)। स्थिति फसल माध्य के ±सहन से तय होती है "
            "(N ±10, P ±5, K ±5, pH ±0.3):\n"
            "{lines}"
        ),
        "SOIL_ANALYSIS_LINE": "• {nutrient}: {current}{unit} — {status} (आदर्श {ideal}{unit})",
        "SOIL_IMBALANCE_HEADER": "लक्ष्य फसल {crop} के मुकाबले {count} असंतुलन:",
        "SOIL_IMBALANCE_LINE": (
            "• {nutrient}: {current}{unit} {status} है (आदर्श {ideal}{unit})। {action}"
        ),
        "SOIL_ALL_OPTIMAL": (
            "{crop} के लिए मापे गए सभी पोषक तत्व निर्धारित सहन सीमा में हैं। "
            "यह मॉडल सीमा से मेल है, खेत की उपज की गारंटी नहीं।"
        ),
        "SOIL_ACTION_LOW": "इस पोषक तत्व की पूर्ति पर विचार करें ({crop} की खाद योजना देखें)।",
        "SOIL_ACTION_HIGH": "इस मौसम यह पोषक तत्व और न डालें।",
        "SOIL_ACTION_OK": "इस पैरामीटर के लिए सुधार की आवश्यकता नहीं।",
        "YIELD_UNAVAILABLE": (
            "इस विश्लेषण में {crop} का उपज अनुमान संग्रहीत नहीं है। "
            "मैं संख्या नहीं बनाऊँगा। समर्थित फसलें: {crops}।"
        ),
        "YIELD_PREDICTION_BOTH": (
            "ये मॉडल अनुमान हैं, गारंटीशुदा फसल नहीं।\n"
            "• लक्ष्य फसल {target}: {target_yield:,.1f} kg/ha\n"
            "• अनुशंसित फसल {recommended}: {recommended_yield:,.1f} kg/ha"
        ),
        "YIELD_ESTIMATE_NOTE": " यह kg/ha में मॉडल अनुमान है, गारंटीशुदा उपज नहीं।",
        "FERTILIZER_OTHER_CROP": (
            "इस विश्लेषण की खाद योजना लक्ष्य फसल {target} के लिए है, {crop} के लिए नहीं। "
            "{crop} की खाद जानकारी के लिए उसे लक्ष्य फसल चुनकर विश्लेषण फिर चलाएँ।"
        ),
        "GROWN_CROP_NONE": "इस विश्लेषण के लिए वास्तव में उगाई गई फसल अभी दर्ज नहीं है।",
        "GROWN_CROP_IS": "इस रन के लिए दर्ज वास्तविक उगाई फसल {crop} है।",
        "NUTRIENT_NO_ADJUSTMENT": (
            "आपका {nutrient} स्तर {value}{unit} है। लेकिन स्मार्ट एग्री के पास {crop} के लिए मिट्टी समायोजन डेटा नहीं है, इसलिए यह नहीं बता सकता कि मान कम, अधिक या उपयुक्त है।"
        ),
        "NUTRIENT_STATUS": (
            "{prefix}आपका {nutrient} स्तर {current}{unit} है। {crop} के लिए स्मार्ट एग्री का आदर्श मान {ideal}{unit} है। आपकी स्थिति {status} है।"
        ),
        "SOIL_STATUS_EXPLANATION": (
            "स्मार्ट एग्री मिट्टी की तीन स्थितियाँ उपयोग करता है:\n"
            "• कम — वर्तमान मान आदर्श सीमा से नीचे है।\n"
            "• अधिक — वर्तमान मान आदर्श सीमा से ऊपर है।\n"
            "• उपयुक्त — मान निर्धारित सहन सीमा में है।"
        ),
        "FERTILIZER_UNSUPPORTED": (
            "स्मार्ट एग्री के पास अभी {crop} के लिए खाद सिफारिश नहीं है। खाद मॉड्यूल इन फसलों को समर्थन देता है: {supported}।"
        ),
        "FERTILIZER_BALANCED": "{prefix}{crop} के लिए आपकी मिट्टी संतुलित है। अभी पोषक सुधार की आवश्यकता नहीं है।",
        "FERTILIZER_BASED": "{prefix}आपके मिट्टी विश्लेषण के आधार पर:",
        "FERTILIZER_CONDITION_LINE": "• {nutrient} {status} है → {label}",
        "FERTILIZER_PRIMARY": "\n{crop} के लिए मुख्य खाद: {fertilizer}",
        "FERTILIZER_DOSAGE_UNSUPPORTED": "स्मार्ट एग्री के पास अभी {crop} के लिए खाद मात्रा डेटा नहीं है।",
        "FERTILIZER_DOSAGE_NONE": "{prefix}{crop} के लिए अभी विशेष खाद मात्रा की आवश्यकता नहीं है क्योंकि मिट्टी उपयुक्त सीमा में है।",
        "FERTILIZER_DOSAGE_HEADER": "{prefix}सुझाई गई खाद मात्रा:",
        "FERTILIZER_DOSAGE_LINE": "• {label}: {dose}",
        "WHY_FERT_UNSUPPORTED": "स्मार्ट एग्री के पास अभी {crop} के लिए खाद डेटा नहीं है।",
        "WHY_FERT_NONE": "{prefix}{crop} के लिए सुधारात्मक खाद की आवश्यकता नहीं है क्योंकि मिट्टी के मान उपयुक्त सीमा में हैं।",
        "WHY_FERT_HEADER": "{prefix}प्रत्येक सिफारिश का कारण:",
        "WHY_FERT_LINE": "• {label}: {reason}",
        "FERT_EXPLAIN_NONE": "{prefix}{crop} के लिए अभी कोई सुधारात्मक खाद सिफारिश नहीं है।",
        "FERT_EXPLAIN_HEADER": "{prefix}आपकी खाद सिफारिशें:",
        "FERT_EXPLAIN_LOW": "• {label} ({npk}) — {reason}",
        "FERT_EXPLAIN_HIGH": "• {label} — {reason}",
        "FERT_EXPLAIN_LINE": "• {label} ({npk}) — {reason}",
        "YIELD_NONE": "स्मार्ट एग्री के पास अभी {crop} के लिए उपज अनुमान नहीं है।",
        "YIELD_PREDICTION": (
            "{prefix}{crop} के लिए अनुमानित उपज {yield_kg:,.1f} kg/ha है। "
            "यह मॉडल अनुमान है, गारंटीशुदा उपज नहीं।"
        ),
        "YIELD_INTERP_NONE": "स्मार्ट एग्री के पास अभी {crop} के लिए उपज व्याख्या नहीं है।",
        "YIELD_LOW": "कम उपज — मिट्टी में काफी सुधार की आवश्यकता है।",
        "YIELD_MOD": "मध्यम उपज — सुधार संभव है।",
        "YIELD_GOOD": "अच्छी उपज — स्थितियाँ अनुकूल हैं।",
        "YIELD_HIGH": "उच्च उपज — उत्कृष्ट स्थितियाँ (गन्ने की सामान्य सीमा)।",
        "YIELD_FACTORS": (
            "उपज अनुमान आपकी विश्लेषण जानकारी का उपयोग करता है: नाइट्रोजन, फॉस्फोरस, पोटैशियम, तापमान, वर्षा, pH और चुनी हुई फसल।"
        ),
        "YIELD_STATUS_EXPLANATION": (
            "स्मार्ट एग्री अनुमानित उपज को मध्यम, अच्छी और उच्च जैसी श्रेणियों में बाँटता है। ये चुनी हुई फसल के लिए मॉडल की व्याख्या हैं।"
        ),
        "OUT_OF_SCOPE": (
            "मैं विशेष रूप से स्मार्ट एग्री के लिए बना हूँ। मैं सॉफ्टवेयर, मिट्टी विश्लेषण, फसल सिफारिश, खाद सिफारिश और उपज अनुमान के प्रश्न का उत्तर दे सकता हूँ।"
        ),
        "UNKNOWN": "मुझे समझ नहीं आया। फसल सिफारिश, मिट्टी, खाद या उपज के बारे में पूछें।",
        "FALLBACK": "इसका उत्तर अभी मेरे पास नहीं है। कृपया स्मार्ट एग्री से जुड़ा प्रश्न पूछें।",
        "OVERRIDE_PREFIX": "(ध्यान दें: आपकी रिपोर्ट की शीर्ष सिफारिश {chosen} है, लेकिन यह विश्लेषण {crop} के लिए है।)\n\n",
    },
    "mr": {
        "GREETING": (
            "नमस्कार! मी स्मार्ट अॅग्री सहाय्यक आहे. "
            "मी तुम्हाला पीक शिफारस, माती विश्लेषण, खत शिफारस आणि उत्पादनाचा अंदाज समजून घेण्यास मदत करू शकतो."
        ),
        "HELP": (
            "मी यामध्ये मदत करू शकतो:\n"
            "• पीक शिफारस\n"
            "• पीक शक्यता टक्केवारी\n"
            "• मातीतील अन्नद्रव्य स्थिती\n"
            "• खत शिफारस\n"
            "• खताचे प्रमाण आणि वापर\n"
            "• उत्पादन अंदाज आणि अर्थ\n\n"
            "तुम्ही विशिष्ट पिकाचे नाव विचारू शकता, उदा. "
            "\"ज्वारीसाठी कोणते खत\" — जरी ती सध्याची सर्वोच्च शिफारस नसली तरी."
        ),
        "SYSTEM_OVERVIEW": (
            "स्मार्ट अॅग्री ही निर्णय-सहाय्य प्रणाली आहे. ती तुमची माती आणि हवामान माहिती वापरून योग्य पीक सुचवते, अन्नद्रव्य तफावत सांगते, खत सुचवते आणि उत्पादनाचा अंदाज देते."
        ),
        "HOW_TO_USE": (
            "स्मार्ट अॅग्री कसे वापरावे:\n"
            "1. नायट्रोजन, फॉस्फरस, पोटॅशियम, pH, तापमान आणि पाऊस सेट करा.\n"
            "2. खत आणि उत्पादनासाठी लक्ष्य पीक निवडा.\n"
            "3. विश्लेषण चालवा वर क्लिक करा.\n"
            "4. डॅशबोर्डवर पीक, माती, खत आणि उत्पादन पहा.\n"
            "5. इंग्रजी, हिंदी किंवा मराठीत मला प्रश्न विचारा."
        ),
        "DASHBOARD": (
            "डॅशबोर्ड एका पानावर विश्लेषण दाखवतो: पीक क्रम, पिकाच्या आदर्शाशी मातीची तुलना, खत सल्ला आणि उत्पादन आलेख. आधी विश्लेषण चालवा, नंतर विभाग पहा किंवा मला निकालाबद्दल विचारा."
        ),
        "ML_MODEL_EXPLANATION": (
            "स्मार्ट अॅग्री पीक शिफारसीसाठी रँडम फॉरेस्ट वर्गीकरण मॉडेल आणि उत्पादनासाठी रँडम फॉरेस्ट रिग्रेशन मॉडेल वापरते. मातीतील तफावत आणि खत सल्ला प्रत्येक पिकाच्या आदर्श अन्नद्रव्य मर्यादांवर आधारित नियम आहेत."
        ),
        "SUPPORTED_CROPS": "स्मार्ट अॅग्री सध्या या पिकांसाठी माती समायोजन आणि खत शिफारस देते: {crops}.",
        "SUPPORTED_CROPS_EMPTY": "सध्या समर्थित पिकांची यादी उपलब्ध नाही. कृपया स्मार्ट अॅग्री डॅशबोर्ड पहा.",
        "CROP_RECOMMENDATION": "तुमच्या सध्याच्या माती आणि पर्यावरण माहितीनुसार, स्मार्ट अॅग्री सर्वोत्तम पीक म्हणून {crop} सुचवते.",
        "CROP_RECOMMENDATION_EXPLANATION": (
            "{crop} सुचवले कारण पीक मॉडेलमध्ये त्याची शक्यता सर्वाधिक {probability:.1f}% होती."
        ),
        "CROP_RECOMMENDATION_EXPLANATION_NO_PROBS": (
            "{crop} तुमच्या माती आणि पर्यावरण माहितीनुसार सर्वात योग्य ठरले, पण तपशीलवार शक्यता यादी सध्या उपलब्ध नाही."
        ),
        "CROP_PROBABILITY_HEADER": "शीर्ष पीक अंदाज हे आहेत:",
        "CROP_PROBABILITY_EMPTY": "या अहवालासाठी पीक शक्यता तपशील उपलब्ध नाही.",
        "CROP_PROBABILITY_LINE": "• {crop}: {probability:.1f}%",
        "CROP_SOIL_UNSUPPORTED": "स्मार्ट अॅग्रीकडे {crop} साठी माती सुसंगतता डेटा नाही. समर्थित पिके: {supported}.",
        "CROP_SOIL_MATCH": "{prefix}तुमची माती {crop} साठी चांगली जुळते — मोजलेली सर्व अन्नद्रव्ये योग्य मर्यादेत आहेत.",
        "CROP_SOIL_MISMATCH": "{prefix}{crop} साठी तुमच्या मातीत काही तफावत आहेत:\n{lines}",
        "CROP_MISMATCH_BETTER": (
            "थोडी विसंगती असू शकते — तुमच्या मातीसाठी, {top_crop} ने तुम्ही निवडलेल्या "
            "{crop} पेक्षा जास्त गुण मिळवले. {top_crop} साठी खत आणि उत्पादन मार्गदर्शन "
            "पाहण्यासाठी लक्ष्य पीक निवडीत ते बदला."
        ),
        "CROP_MISMATCH_BEST": "तुमच्या माती आणि हवामान माहितीसाठी सध्या {crop} हेच सर्वोत्तम जुळणारे पीक आहे.",
        "SOIL_MISMATCH_LINE": "• {nutrient} {status} आहे (सध्या: {current}, आदर्श: {ideal})",
        "SOIL_ANALYSIS": (
            "लक्ष्य पीक {crop} च्या आदर्श मर्यादेच्या तुलनेत माती विश्लेषण "
            "(N, P, K kg/ha मध्ये; pH एककरहित). स्थिती पिकाच्या सरासरी ±सहनने ठरते "
            "(N ±10, P ±5, K ±5, pH ±0.3):\n"
            "{lines}"
        ),
        "SOIL_ANALYSIS_LINE": "• {nutrient}: {current}{unit} — {status} (आदर्श {ideal}{unit})",
        "SOIL_IMBALANCE_HEADER": "लक्ष्य पीक {crop} च्या तुलनेत {count} असंतुलने:",
        "SOIL_IMBALANCE_LINE": (
            "• {nutrient}: {current}{unit} {status} आहे (आदर्श {ideal}{unit}). {action}"
        ),
        "SOIL_ALL_OPTIMAL": (
            "{crop} साठी मोजलेली सर्व अन्नद्रव्ये ठरवलेल्या सहन मर्यादेत आहेत. "
            "ही मॉडेल मर्यादेशी जुळणी आहे, शेतातील उत्पादनाची हमी नाही."
        ),
        "SOIL_ACTION_LOW": "हे अन्नद्रव्य पुरवण्याचा विचार करा ({crop} ची खत योजना पहा).",
        "SOIL_ACTION_HIGH": "या हंगामात हे अन्नद्रव्य अधिक टाकू नका.",
        "SOIL_ACTION_OK": "या घटकासाठी सुधारणा लागणार नाही.",
        "YIELD_UNAVAILABLE": (
            "या विश्लेषणात {crop} साठी उत्पादन अंदाज साठवलेला नाही. "
            "मी संख्या बनवणार नाही. समर्थित पिके: {crops}."
        ),
        "YIELD_PREDICTION_BOTH": (
            "हे मॉडेल अंदाज आहेत, हमी दिलेले उत्पादन नाही.\n"
            "• लक्ष्य पीक {target}: {target_yield:,.1f} kg/ha\n"
            "• शिफारस केलेले पीक {recommended}: {recommended_yield:,.1f} kg/ha"
        ),
        "YIELD_ESTIMATE_NOTE": " हे kg/ha मधील मॉडेल अंदाज आहे, हमी दिलेले उत्पादन नाही.",
        "FERTILIZER_OTHER_CROP": (
            "या विश्लेषणातील खत योजना लक्ष्य पीक {target} साठी आहे, {crop} साठी नाही. "
            "{crop} ची खत माहिती मिळवण्यासाठी ते लक्ष्य पीक निवडून विश्लेषण पुन्हा चालवा."
        ),
        "GROWN_CROP_NONE": "या विश्लेषणासाठी खरे पिकवलेले पीक अद्याप नोंदलेले नाही.",
        "GROWN_CROP_IS": "या रनसाठी नोंदलेले खरे पिकवलेले पीक {crop} आहे.",
        "NUTRIENT_NO_ADJUSTMENT": (
            "तुमची {nutrient} पातळी {value}{unit} आहे. पण स्मार्ट अॅग्रीकडे {crop} साठी माती समायोजन डेटा नाही, त्यामुळे हे मूल्य कमी, जास्त की योग्य ते सांगता येत नाही."
        ),
        "NUTRIENT_STATUS": (
            "{prefix}तुमची {nutrient} पातळी {current}{unit} आहे. {crop} साठी स्मार्ट अॅग्रीचा आदर्श मूल्य {ideal}{unit} आहे. तुमची स्थिती {status} आहे."
        ),
        "SOIL_STATUS_EXPLANATION": (
            "स्मार्ट अॅग्री मातीच्या तीन स्थिती वापरते:\n"
            "• कमी — सध्याचे मूल्य आदर्श मर्यादेपेक्षा कमी आहे.\n"
            "• जास्त — सध्याचे मूल्य आदर्श मर्यादेपेक्षा जास्त आहे.\n"
            "• योग्य — मूल्य ठरवलेल्या सहन मर्यादेत आहे."
        ),
        "FERTILIZER_UNSUPPORTED": (
            "स्मार्ट अॅग्रीकडे सध्या {crop} साठी खत शिफारस नाही. खत मॉड्यूल ही पिके समर्थन करते: {supported}."
        ),
        "FERTILIZER_BALANCED": "{prefix}{crop} साठी तुमची माती संतुलित आहे. सध्या अन्नद्रव्य सुधारणेची गरज नाही.",
        "FERTILIZER_BASED": "{prefix}तुमच्या माती विश्लेषणानुसार:",
        "FERTILIZER_CONDITION_LINE": "• {nutrient} {status} आहे → {label}",
        "FERTILIZER_PRIMARY": "\n{crop} साठी मुख्य खत: {fertilizer}",
        "FERTILIZER_DOSAGE_UNSUPPORTED": "स्मार्ट अॅग्रीकडे सध्या {crop} साठी खत प्रमाण डेटा नाही.",
        "FERTILIZER_DOSAGE_NONE": "{prefix}{crop} साठी सध्या खास खत प्रमाण लागणार नाही कारण माती योग्य मर्यादेत आहे.",
        "FERTILIZER_DOSAGE_HEADER": "{prefix}शिफारस केलेले खत प्रमाण:",
        "FERTILIZER_DOSAGE_LINE": "• {label}: {dose}",
        "WHY_FERT_UNSUPPORTED": "स्मार्ट अॅग्रीकडे सध्या {crop} साठी खत डेटा नाही.",
        "WHY_FERT_NONE": "{prefix}{crop} साठी सुधारात्मक खताची गरज नाही कारण मातीची मूल्ये योग्य मर्यादेत आहेत.",
        "WHY_FERT_HEADER": "{prefix}प्रत्येक शिफारसीचे कारण:",
        "WHY_FERT_LINE": "• {label}: {reason}",
        "FERT_EXPLAIN_NONE": "{prefix}{crop} साठी सध्या सुधारात्मक खत शिफारस नाही.",
        "FERT_EXPLAIN_HEADER": "{prefix}तुमच्या खत शिफारसी:",
        "FERT_EXPLAIN_LOW": "• {label} ({npk}) — {reason}",
        "FERT_EXPLAIN_HIGH": "• {label} — {reason}",
        "FERT_EXPLAIN_LINE": "• {label} ({npk}) — {reason}",
        "YIELD_NONE": "स्मार्ट अॅग्रीकडे सध्या {crop} साठी उत्पादन अंदाज नाही.",
        "YIELD_PREDICTION": (
            "{prefix}{crop} साठी अंदाजित उत्पादन {yield_kg:,.1f} kg/ha आहे. "
            "हा मॉडेल अंदाज आहे, हमी दिलेले उत्पादन नाही."
        ),
        "YIELD_INTERP_NONE": "स्मार्ट अॅग्रीकडे सध्या {crop} साठी उत्पादन व्याख्या नाही.",
        "YIELD_LOW": "कमी उत्पादन — मातीत मोठी सुधारणा आवश्यक आहे.",
        "YIELD_MOD": "मध्यम उत्पादन — सुधारणा शक्य आहे.",
        "YIELD_GOOD": "चांगले उत्पादन — परिस्थिती अनुकूल आहे.",
        "YIELD_HIGH": "उच्च उत्पादन — उत्कृष्ट परिस्थिती (ऊसाची नेहमीची मर्यादा).",
        "YIELD_FACTORS": (
            "उत्पादन अंदाज तुमच्या विश्लेषणातील माती आणि पर्यावरण माहिती वापरतो: नायट्रोजन, फॉस्फरस, पोटॅशियम, तापमान, पाऊस, pH आणि निवडलेले पीक."
        ),
        "YIELD_STATUS_EXPLANATION": (
            "स्मार्ट अॅग्री अंदाजित उत्पादनाला मध्यम, चांगले आणि उच्च या श्रेणीत वर्गीकृत करते. या निवडलेल्या पिकासाठी मॉडेलची व्याख्या आहेत."
        ),
        "OUT_OF_SCOPE": (
            "मी फक्त स्मार्ट अॅग्रीसाठी बनवला आहे. मी सॉफ्टवेअर, माती विश्लेषण, पीक शिफारस, खत शिफारस आणि उत्पादन अंदाजाबद्दलचे प्रश्न उत्तर देऊ शकतो."
        ),
        "UNKNOWN": "मला प्रश्न समजला नाही. पीक शिफारस, माती, खत किंवा उत्पादनाबद्दल विचारा.",
        "FALLBACK": "याचे उत्तर सध्या माझ्याकडे नाही. कृपया स्मार्ट अॅग्रीशी संबंधित प्रश्न विचारा.",
        "OVERRIDE_PREFIX": "(टीप: तुमच्या अहवालातील सर्वोच्च शिफारस {chosen} आहे, पण हे विश्लेषण {crop} साठी आहे.)\n\n",
    },
}


def crop_name(crop, lang):
    names = CROP_DISPLAY.get(crop)
    if not names:
        return crop
    return names.get(lang, names["en"])


def nutrient_name(nutrient, lang):
    names = NUTRIENT_DISPLAY.get(nutrient)
    if not names:
        return nutrient
    return names.get(lang, names["en"])


def status_name(status, lang):
    names = STATUS_DISPLAY.get(status)
    if not names:
        return status
    return names.get(lang, names["en"])


# Extra keys: on-demand yield and per-crop fertilizer (kept together for clarity).
_MESSAGES["en"].update({
    "YIELD_CALCULATED": (
        "Estimated yield for {crop} is {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha). "
        "No saved prediction existed for {crop} in this analysis, so I calculated it now "
        "with the yield model using your soil readings. It is a model estimate, not a guaranteed harvest."
    ),
    "YIELD_SAVED": (
        "Saved estimate for {crop} in this analysis: {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha). "
        "It is a model estimate, not a guaranteed harvest."
    ),
    "YIELD_NOT_POSSIBLE": (
        "A yield estimate for {crop} is not available for this analysis, and the yield model "
        "cannot calculate one for it. I will not invent a number. Crops with yield estimates: {crops}."
    ),
    "FERT_REC_HEADER": "Fertilizer advice for the recommended crop {crop}:",
    "FERT_REC_UNAVAILABLE": (
        "Fertilizer advice for the recommended crop {crop} is not available "
        "(the fertilizer rules do not cover this crop), so I cannot give quantities."
    ),
})
_MESSAGES["hi"].update({
    "YIELD_CALCULATED": (
        "{crop} का अनुमानित उत्पादन {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha) है। "
        "इस विश्लेषण में {crop} का सहेजा हुआ अनुमान नहीं था, इसलिए मैंने आपकी मिट्टी की रीडिंग से "
        "उपज मॉडल द्वारा अभी गणना की है। यह मॉडल अनुमान है, पक्की उपज नहीं।"
    ),
    "YIELD_SAVED": (
        "इस विश्लेषण में {crop} का सहेजा हुआ अनुमान: {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha)। "
        "यह मॉडल अनुमान है, पक्की उपज नहीं।"
    ),
    "YIELD_NOT_POSSIBLE": (
        "इस विश्लेषण के लिए {crop} का उपज अनुमान उपलब्ध नहीं है और उपज मॉडल इसकी गणना नहीं कर सकता। "
        "मैं कोई संख्या नहीं बनाऊँगा। उपज अनुमान वाली फसलें: {crops}।"
    ),
    "FERT_REC_HEADER": "अनुशंसित फसल {crop} के लिए खाद सलाह:",
    "FERT_REC_UNAVAILABLE": (
        "अनुशंसित फसल {crop} के लिए खाद सलाह उपलब्ध नहीं है (खाद नियम इस फसल को कवर नहीं करते), "
        "इसलिए मैं मात्रा नहीं बता सकता।"
    ),
})
_MESSAGES["mr"].update({
    "YIELD_CALCULATED": (
        "{crop} साठी अंदाजित उत्पादन {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha) आहे. "
        "या विश्लेषणात {crop} चा साठवलेला अंदाज नव्हता, म्हणून तुमच्या मातीच्या नोंदींवरून "
        "उत्पादन मॉडेलने आता तो काढला आहे. हा मॉडेल अंदाज आहे, हमी दिलेले उत्पादन नाही."
    ),
    "YIELD_SAVED": (
        "या विश्लेषणात {crop} साठी साठवलेला अंदाज: {yield_kg:,.1f} kg/ha ({yield_t:,.2f} t/ha). "
        "हा मॉडेल अंदाज आहे, हमी दिलेले उत्पादन नाही."
    ),
    "YIELD_NOT_POSSIBLE": (
        "या विश्लेषणासाठी {crop} पिकाचे उत्पादन अद्याप अंदाजित केलेले नाही आणि उत्पादन मॉडेल ते काढू शकत नाही. "
        "मी कोणताही आकडा तयार करणार नाही. उत्पादन अंदाज असलेली पिके: {crops}."
    ),
    "FERT_REC_HEADER": "शिफारस केलेल्या पीक {crop} साठी खत सल्ला:",
    "FERT_REC_UNAVAILABLE": (
        "शिफारस केलेल्या पीक {crop} साठी खत सल्ला उपलब्ध नाही (खत नियम या पिकाला लागू नाहीत), "
        "त्यामुळे मी प्रमाण सांगू शकत नाही."
    ),
})


def msg(lang, key, **kwargs):
    bundle = _MESSAGES.get(lang, _MESSAGES["en"])
    template = bundle.get(key) or _MESSAGES["en"].get(key, "")
    if kwargs:
        return template.format(**kwargs)
    return template


FERT_PHRASE = {
    "Apply in 2 splits — basal + top-dress at 30 days": {
        "hi": "2 भागों में डालें — बुवाई के समय और 30 दिन बाद",
        "mr": "2 हप्त्यांत टाका — पेरणीवेळी आणि 30 दिवसांनी",
    },
    "Apply as basal dose at sowing": {
        "hi": "बुवाई के समय आधार मात्रा में डालें",
        "mr": "पेरणीवेळी मूळ मात्रा म्हणून टाका",
    },
    "Apply at basal or after 30 days of sowing": {
        "hi": "बुवाई के समय या 30 दिन बाद डालें",
        "mr": "पेरणीवेळी किंवा 30 दिवसांनी टाका",
    },
    "Skip N fertilizer this season; allow soil to deplete naturally": {
        "hi": "इस मौसम नाइट्रोजन खाद न डालें; मिट्टी अपने आप घटे",
        "mr": "या हंगामात नायट्रोजन खत टाकू नका; माती नैसर्गिकरीत्या कमी होऊ द्या",
    },
    "Avoid phosphate fertilizers this season": {
        "hi": "इस मौसम फॉस्फेट खाद से बचें",
        "mr": "या हंगामात फॉस्फेट खते टाळा",
    },
    "Skip potash fertilizer this season": {
        "hi": "इस मौसम पोटाश खाद न डालें",
        "mr": "या हंगामात पालाश खत टाकू नका",
    },
    "Apply 1–2 tonnes/ha and incorporate into soil before sowing": {
        "hi": "बुवाई से पहले 1–2 टन/हेक्टेयर मिट्टी में मिलाएँ",
        "mr": "पेरणीपूर्वी 1–2 टन/हेक्टर मातीत मिसळा",
    },
    "Apply elemental sulphur @ 20–30 kg/ha": {
        "hi": "गंधक 20–30 किग्रा/हेक्टेयर डालें",
        "mr": "गंधक 20–30 किग्रॅ/हेक्टर टाका",
    },
    "Urea is the most concentrated and economical N source (46% N).": {
        "hi": "यूरिया सबसे सघन और किफायती नाइट्रोजन स्रोत है (46% N)।",
        "mr": "युरिया सर्वात संहत आणि किफायतशीर नायट्रोजन स्रोत आहे (46% N).",
    },
    "DAP provides both N and P; ideal for root development.": {
        "hi": "डीएपी में नाइट्रोजन और फॉस्फोरस दोनों हैं; जड़ विकास के लिए उपयुक्त।",
        "mr": "डीएपीमध्ये नायट्रोजन आणि फॉस्फरस दोन्ही आहेत; मुळांच्या वाढीसाठी योग्य.",
    },
    "MOP is the most concentrated and affordable K source (60% K₂O).": {
        "hi": "एमओपी सबसे सघन और सस्ता पोटैशियम स्रोत है (60% K₂O)।",
        "mr": "एमओपी सर्वात संहत आणि स्वस्त पोटॅशियम स्रोत आहे (60% K₂O).",
    },
    "Excess N causes vegetative overgrowth and reduces grain yield.": {
        "hi": "अधिक नाइट्रोजन से ज्यादा हरियाली होती है और दाने की उपज घटती है।",
        "mr": "जास्त नायट्रोजनमुळे पानांची अतिवाढ होते आणि दाण्याचे उत्पादन घटते.",
    },
    "Excess P locks out zinc and iron micronutrients.": {
        "hi": "अधिक फॉस्फोरस जिंक और आयरन को बाधित करता है।",
        "mr": "जास्त फॉस्फरस झिंक आणि लोह उपलब्धता कमी करतो.",
    },
    "Excess K inhibits magnesium and calcium uptake.": {
        "hi": "अधिक पोटैशियम मैग्नीशियम और कैल्शियम ग्रहण घटाता है।",
        "mr": "जास्त पोटॅशियम मॅग्नेशियम आणि कॅल्शियम घेणे कमी करते.",
    },
    "Acidic soil makes P unavailable; lime raises pH toward neutral.": {
        "hi": "अम्लीय मिट्टी में फॉस्फोरस उपलब्ध नहीं रहता; चूना pH को सामान्य की ओर लाता है।",
        "mr": "आम्ल मातीत फॉस्फरस उपलब्ध राहत नाही; चुनखडी pH सामान्यकडे नेते.",
    },
    "Alkaline soil reduces Fe/Mn availability; sulphur acidifies soil.": {
        "hi": "क्षारीय मिट्टी में लोहा/मैंगनीज कम मिलता है; गंधक मिट्टी को अम्लीय बनाता है।",
        "mr": "क्षारीय मातीत लोह/मॅंगनीज कमी मिळते; गंधक माती आम्ल करते.",
    },
}


def format_crop_list(crops, lang):
    return ", ".join(crop_name(crop, lang) for crop in crops)


def fert_phrase(text, lang):
    if not text or lang == "en":
        return text
    mapped = FERT_PHRASE.get(text)
    if not mapped:
        return text
    return mapped.get(lang, text)
