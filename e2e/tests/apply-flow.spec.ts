import { expect, test } from "@playwright/test";

const WORDS_100 = Array.from({ length: 100 }, (_, i) => `w${i}`).join(" ");

test.describe("Apply flow — client-side smoke", () => {
  test("form blocks submission until all 100-word answers are filled", async ({ page }) => {
    // Intercept the submit so we don't need the backend running for the smoke
    await page.route("**/applications", (route) =>
      route.fulfill({
        status: 201,
        contentType: "application/json",
        body: JSON.stringify({ id: 1, status: "submitted" }),
      }),
    );

    await page.goto("/academy/apply");

    // Hero renders with the numbered label + display heading
    await expect(page.getByText(/Aplicaci[oó]n · cohorte/i)).toBeVisible();

    // Submit button starts disabled
    const submit = page.getByRole("button", { name: /enviar aplicaci/i });
    await expect(submit).toBeDisabled();

    // Fill top-of-form fields
    await page.getByLabel(/nombre completo/i).fill("Ana Ejemplo");
    await page.getByLabel(/^email/i).fill("ana@example.com");
    await page.getByLabel(/url de video/i).fill("https://loom.com/share/abc");

    // Fill the three open-ended answers with exactly 100 words
    const textareas = page.getByRole("textbox", { name: /quiere|logro|horas/i });
    await expect(textareas).toHaveCount(3);
    for (let i = 0; i < 3; i++) {
      await textareas.nth(i).fill(WORDS_100);
    }

    // At least one "100/100" counter appears
    await expect(page.getByText(/100\/100/).first()).toBeVisible();

    await expect(submit).toBeEnabled();
    await submit.click();

    // The success state appears after submit
    await expect(
      page.getByText(/tu aplicaci[oó]n est[aá] en nuestra mesa/i),
    ).toBeVisible();
  });

  test("homepage hero renders and links to apply", async ({ page }) => {
    await page.goto("/academy/");
    await expect(page.getByRole("heading", { level: 1 })).toContainText(
      /la formaci[oó]n/i,
    );
    await page.getByRole("link", { name: /aplica a la cohorte/i }).click();
    await expect(page).toHaveURL(/\/academy\/apply/);
  });
});
