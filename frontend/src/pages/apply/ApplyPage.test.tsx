import { describe, expect, it, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { screen } from "@testing-library/react";

import { ApplyPage } from "./ApplyPage";
import { renderWithProviders } from "@/test/renderWithProviders";

vi.mock("@/lib/api", () => ({
  api: {
    post: vi.fn().mockResolvedValue({ data: { id: 1 } }),
  },
}));

import { api } from "@/lib/api";

const wordsOf = (n: number) =>
  Array.from({ length: n }, (_, i) => `w${i}`).join(" ");

describe("ApplyPage — admission form", () => {
  it("submit button is disabled until every answer reaches 100 words", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);

    const submit = screen.getByRole("button", { name: /enviar aplicaci/i });
    expect(submit).toBeDisabled();

    await user.type(screen.getByLabelText(/nombre completo/i), "Ana");
    await user.type(screen.getByLabelText(/^email/i), "ana@example.com");
    await user.type(screen.getByLabelText(/url de video/i), "https://loom.com/x");

    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    expect(textareas).toHaveLength(3);

    // Fill the first two with 100 words — still short on the third
    await user.type(textareas[0], wordsOf(100));
    await user.type(textareas[1], wordsOf(100));
    await user.type(textareas[2], "too short");
    expect(submit).toBeDisabled();

    // Finish the third
    await user.clear(textareas[2]);
    await user.type(textareas[2], wordsOf(100));
    expect(submit).toBeEnabled();
  }, 30_000);

  it("shows the word counter with correct count and threshold styling", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);
    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    await user.type(textareas[0], wordsOf(50));
    expect(screen.getAllByText(/50\/100/).length).toBeGreaterThan(0);
  }, 20_000);

  it("submits the expected payload when valid", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);

    await user.type(screen.getByLabelText(/nombre completo/i), "Ana");
    await user.type(screen.getByLabelText(/^email/i), "ana@example.com");
    await user.type(screen.getByLabelText(/url de video/i), "https://loom.com/x");

    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    await user.type(textareas[0], wordsOf(100));
    await user.type(textareas[1], wordsOf(100));
    await user.type(textareas[2], wordsOf(100));

    await user.click(screen.getByRole("button", { name: /enviar aplicaci/i }));

    expect(api.post).toHaveBeenCalledWith(
      "/applications",
      expect.objectContaining({
        applicant_name: "Ana",
        applicant_email: "ana@example.com",
        video_url: "https://loom.com/x",
        answers: expect.arrayContaining([
          expect.objectContaining({ question_id: "why_sales" }),
          expect.objectContaining({ question_id: "achievement" }),
          expect.objectContaining({ question_id: "hours_per_week" }),
        ]),
      }),
    );

    expect(await screen.findByText(/tu aplicaci[oó]n est[aá] en nuestra mesa/i)).toBeVisible();
  }, 30_000);
});
