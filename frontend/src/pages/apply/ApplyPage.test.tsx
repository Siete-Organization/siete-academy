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

describe("ApplyPage — admission form", () => {
  it("submit is enabled once required identity fields + video are filled, regardless of answer length", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);

    const submit = screen.getByRole("button", { name: /enviar aplicaci/i });
    expect(submit).toBeDisabled();

    await user.type(screen.getByLabelText(/nombre completo/i), "Ana");
    await user.type(screen.getByLabelText(/^email/i), "ana@example.com");
    await user.type(screen.getByLabelText(/linkedin/i), "https://www.linkedin.com/in/ana");
    await user.type(screen.getByLabelText(/pa[ií]s/i), "Perú");
    await user.type(screen.getByLabelText(/url de video/i), "https://loom.com/x");

    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    await user.type(textareas[0], "uno");
    await user.type(textareas[1], "dos");
    await user.type(textareas[2], "tres");

    expect(submit).toBeEnabled();
  }, 30_000);

  it("shows a plain word counter (informational, not blocking)", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);
    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    await user.type(textareas[0], "una dos tres");
    expect(screen.getAllByText(/3 palabras/).length).toBeGreaterThan(0);
  }, 20_000);

  it("submits the expected payload when required fields are present", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ApplyPage />);

    await user.type(screen.getByLabelText(/nombre completo/i), "Ana");
    await user.type(screen.getByLabelText(/^email/i), "ana@example.com");
    await user.type(screen.getByLabelText(/linkedin/i), "https://www.linkedin.com/in/ana");
    await user.type(screen.getByLabelText(/pa[ií]s/i), "Perú");
    await user.type(screen.getByLabelText(/url de video/i), "https://loom.com/x");

    const textareas = screen.getAllByRole("textbox", { name: /quiere|logro|horas/i });
    await user.type(textareas[0], "uno");
    await user.type(textareas[1], "dos");
    await user.type(textareas[2], "tres");

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
