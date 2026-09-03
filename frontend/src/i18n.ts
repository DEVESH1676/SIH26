/**
 * Multi-language i18n configuration.
 * Supports English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Urdu, etc.
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

const resources = {
  en: {
    translation: {
      nav: { home: 'Home', courses: 'Courses', quizzes: 'Quizzes', analytics: 'Analytics', profile: 'Profile' },
      dashboard: { welcome: 'Welcome, {{name}}', your_progress: 'Your Learning Progress', recommended: 'Recommended for You', skill_gaps: 'Skill Gaps Identified' },
      course: { title: 'Title', duration: 'Duration', difficulty: 'Difficulty', enroll: 'Enroll Now', start: 'Start Course', progress: 'Progress' },
      quiz: { take_quiz: 'Take Quiz', submit: 'Submit Answers', score: 'Score', pass: 'Pass', fail: 'Try Again', explanation: 'Explanation' },
      upload: { upload_file: 'Upload Learning Material', supported_formats: 'Supported: PDF, DOCX, PPTX, MP4, MP3', generate_quiz: 'Generate Quiz' },
      admin: { overview: 'Overview', workforce: 'Workforce Analytics', training: 'Training Effectiveness', predictive: 'Predictive Insights' },
      assistant: { type_message: 'Type your question...', response: 'Assistant Response', suggest: 'Suggestions' },
    },
  },
  hi: {
    translation: {
      nav: { home: 'होम', courses: 'कोर्सेज', quizzes: 'क्विज़', analytics: 'विश्लेषण', profile: 'प्रोफ़ाइल' },
      dashboard: { welcome: 'स्वागत है, {{name}}', your_progress: 'आपकी शिक्षा प्रगति', recommended: 'आपके लिए अनुशंसित', skill_gaps: 'कौशल अंतर पहचाने गए' },
      course: { title: 'शीर्षक', duration: 'अवधि', difficulty: 'कठिनाई', enroll: 'अभी नामांकन करें', start: 'कोर्स शुरू करें', progress: 'प्रगति' },
      quiz: { take_quiz: 'क्विज़ लें', submit: 'उत्तर जमा करें', score: 'अंक', pass: 'पार', fail: 'फिर से प्रयास करें', explanation: 'व्याख्या' },
      upload: { upload_file: 'शिक्षा सामग्री अपलोड करें', supported_formats: 'समर्थित: PDF, DOCX, PPTX, MP4, MP3', generate_quiz: 'क्विज़ उत्पन्न करें' },
      admin: { overview: 'अवलोकन', workforce: 'कार्यबल विश्लेषण', training: 'प्रशिक्षण प्रभावकारिता', predictive: 'पूर्वानुमानित अंतर्दृष्टि' },
      assistant: { type_message: 'अपना प्रश्न लिखें...', response: 'सहायक उत्तर', suggest: 'सुझाव' },
    },
  },
  // Add more languages: bn, ta, te, mr, gu, ur, pa, ml, or, etc.
} as const;

i18n.use(LanguageDetector).use(initReactI18next).init({
  resources,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
