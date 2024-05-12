import { test, expect } from '@playwright/test';
import { Page } from '@playwright/test';
import BasePage from './page-object/BasePage'

import ResultsPage from './page-object/ResultsPage'

let basePage: BasePage
let resultPage: ResultsPage

test.describe('Main Page tests', async () => {

  test.beforeEach(async ({ page }: { page: Page }) => {
    basePage = new BasePage(page)
    await basePage.navigateTo()
  });
  test('has title', async ({ page }) => {
    await expect(page).toHaveTitle(/Song Search and Genre Wheel/);
  });
  
  test('search results are present in url', async ({page}) => {
    let textForSearch = 'Zlypni'

    await basePage.typeSearch(textForSearch)
    await basePage.findSong()

    const urlPattern = new RegExp(`${textForSearch}`);
    await expect(page).toHaveURL(urlPattern);
  })
  
  test('search for Genre is disabled by default', async ({page}) => {
    let getGenre = await basePage.getSearchGenreBtn()

    await expect(getGenre).toBeDisabled()
  })

  test('search for Genre is disabled while spinning the wheel', async ({page}) => {
    await basePage.spinWheel()
    let getGenre = await basePage.getSearchGenreBtn()

    await expect(getGenre).toBeDisabled()
  })

  test('spin btn is disables while spinning', async ({page}) => {
    await basePage.spinWheel()
    let spinWheelBtn = await basePage.getspinWheel()
    
    await expect(spinWheelBtn).toBeDisabled()
  })

  test('getGenre leads to top ukrainian song after spinning the wheel', async ({page}) => {
    let getGenre = await basePage.getSearchGenreBtn()

    await basePage.spinWheel()

    //TOTO fix
    await page.waitForSelector(`#searchButton:enabled`);
    let spinnedGenre = (await basePage.getSearchGenreBtn()).textContent()

    await basePage.searchGenre()

    const urlPattern = new RegExp(`${spinnedGenre}`);
    await expect(page).toHaveTitle(urlPattern); 
  })

  test.skip('music defenders redirects to the site', async ({ page }) => {
    const realLink = 'https://musiciansdefendukraine.com/en';

    await basePage.musicalDefendersLink();

    // Wait for navigation to complete
    await page.waitForNavigation();

    // Get the URL of the current page
    const currentUrl = page.url();

    // Check if the current URL matches the expected redirect URL
    expect(currentUrl).toBe(realLink);
  });

  test('empty search', async ({page}) => {
    await basePage.findSong()

    expect(page).toHaveTitle('No Data Found')
  })

  test('go back from no data page', async ({page}) => {
    await basePage.findSong()

    await basePage.noDataGoBack()

    await expect(page).toHaveTitle(/Song Search and Genre Wheel/);
  })
  
})

test.describe('Results Page tests', async () => {
  let searchBase = 'Linkin Park'; 

  test.beforeEach(async ({ page }: { page: Page }) => {
    resultPage = new ResultsPage(page);
    await resultPage.navigateToPage(searchBase);
  });

  test('navigation to result page', async ({ page }) => {
    let title = `Search Results for ${searchBase}`; 

    await expect(page).toHaveTitle(title);
  });

  test('should have 10 songs with popular query', async () => {
    let songsCount = await resultPage.getSongsCards()
    expect(songsCount).toEqual(10)
  })

  test('should have 10 artists with popular query', async () => {
    let artistCount = await resultPage.getArtistsCards()
    expect(artistCount).toEqual(10)
  })

  test('should match text with song card', async () => {
    let songsText = await (await resultPage.getFirstSongCard()).innerText()

    expect(songsText).toContain(searchBase)
  })
  test('should match text with artist card', async () => {
    let songsText = await (await resultPage.getFirstArtistCard()).innerText()

    expect(songsText).toContain(searchBase)
  })
  
  test('should redirect to similar songs', async ({page}) => {
    resultPage.redirectSimilarSongs()

    await page.waitForTimeout(9000)
    let title = /Similar Songs to/; 

    await expect(page).toHaveTitle(title)
  })

  test('should redirect to similar artist', async ({page}) => {
    resultPage.redirectSimilarArtists()

    await page.waitForTimeout(9000)

    let title = `Similar Artists to \"${searchBase}\"`; 

    await expect(page).toHaveTitle(title);
  })
  
  test('should redirect to Spotify', async ({page}) => {
 
  })


  test('should redirect to YoutubeMusic', async ({page}) => {

  });

  test('should redirect to Deezer', async ({page}) => {

  })



  test('should redirect to home page', async ({page}) => {
    resultPage. homeRedirect()

    await expect(page).toHaveTitle(/Song Search and Genre Wheel/);
  })

});

