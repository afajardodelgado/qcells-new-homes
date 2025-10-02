import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should load the home page', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Solar Support Suite');
  });

  test('should navigate between sections', async ({ page }) => {
    await page.goto('/');

    // Check initial section is Homes
    await expect(page.locator('#section-homes')).toBeVisible();
    await expect(page.locator('.nav-item.active')).toContainText('Homes');

    // Navigate to Pricing
    await page.locator('.nav-item[data-section="pricing"]').click();
    await expect(page.locator('#section-pricing')).toBeVisible();
    await expect(page.locator('#section-homes')).not.toBeVisible();
    await expect(page.locator('.nav-item.active')).toContainText('Pricing');

    // Navigate to Marketing
    await page.locator('.nav-item[data-section="marketing"]').click();
    await expect(page.locator('#section-marketing')).toBeVisible();
    await expect(page.locator('#section-pricing')).not.toBeVisible();

    // Navigate to Training
    await page.locator('.nav-item[data-section="training"]').click();
    await expect(page.locator('#section-training')).toBeVisible();

    // Navigate to Support
    await page.locator('.nav-item[data-section="support"]').click();
    await expect(page.locator('#section-support')).toBeVisible();

    // Navigate back to Homes
    await page.locator('.nav-item[data-section="homes"]').click();
    await expect(page.locator('#section-homes')).toBeVisible();
  });

  test('should display navigation icons without emojis', async ({ page }) => {
    await page.goto('/');

    // Check that all nav items have SVG icons instead of emojis
    const navItems = await page.locator('.nav-item .icon svg').count();
    expect(navItems).toBe(5);

    // Verify no emoji characters in navigation
    const navContent = await page.locator('.nav').textContent();
    const emojiRegex = /[\u{1F300}-\u{1F9FF}]/u;
    expect(emojiRegex.test(navContent)).toBe(false);
  });
});

test.describe('Salesforce Query Interface', () => {
  test('should have query input and button', async ({ page }) => {
    await page.goto('/');

    await expect(page.locator('#soql')).toBeVisible();
    await expect(page.locator('#runQuery')).toBeVisible();
    await expect(page.locator('#output')).toBeVisible();
  });

  test('should show default query in input', async ({ page }) => {
    await page.goto('/');

    const queryInput = page.locator('#soql');
    const value = await queryInput.inputValue();
    expect(value).toContain('SELECT');
  });
});

test.describe('UI Compliance', () => {
  test('should have correct Q.CELLS branding', async ({ page }) => {
    await page.goto('/');

    // Check logo is present
    const logo = page.locator('.logo');
    await expect(logo).toBeVisible();
    await expect(logo).toHaveAttribute('alt', 'New Homes Logo');
  });

  test('should have proper layout structure', async ({ page }) => {
    await page.goto('/');

    // Verify sidebar exists
    await expect(page.locator('.sidebar')).toBeVisible();

    // Verify main content area exists
    await expect(page.locator('.content')).toBeVisible();

    // Verify global navigation bar exists
    await expect(page.locator('.gnb')).toBeVisible();
  });
});
