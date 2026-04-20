import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";

import es from "../locales/es/common.json";
import en from "../locales/en/common.json";
import pt from "../locales/pt/common.json";

void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      es: { common: es },
      en: { common: en },
      pt: { common: pt },
    },
    fallbackLng: "es",
    supportedLngs: ["es", "en", "pt"],
    defaultNS: "common",
    interpolation: { escapeValue: false },
  });

export default i18n;
