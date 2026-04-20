import { type ReactElement } from "react";
import { render, type RenderOptions } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import es from "@/locales/es/common.json";
import en from "@/locales/en/common.json";
import pt from "@/locales/pt/common.json";

if (!i18n.isInitialized) {
  void i18n.use(initReactI18next).init({
    resources: {
      es: { common: es },
      en: { common: en },
      pt: { common: pt },
    },
    lng: "es",
    fallbackLng: "es",
    defaultNS: "common",
    interpolation: { escapeValue: false },
  });
}

export function renderWithProviders(
  ui: ReactElement,
  options?: { route?: string } & Omit<RenderOptions, "wrapper">,
) {
  const { route = "/", ...rest } = options ?? {};
  return render(
    <I18nextProvider i18n={i18n}>
      <MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>
    </I18nextProvider>,
    rest,
  );
}
