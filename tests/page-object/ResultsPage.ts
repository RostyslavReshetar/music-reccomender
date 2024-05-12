import {Locator, Page, expect} from "@playwright/test";


import {
  inizializeSongRecomender
} from "./locatorInitializationUtils";
import { songRecomenderProject } from "./interface";

import BasePage from "./BasePage";


export default class ResultsPage extends BasePage {
  readonly page: Page; 
  readonly project: songRecomenderProject

  constructor(page: Page) {
    super(page)
    this.page = page
    this.project = inizializeSongRecomender(page)
  }

  async navigateToPage(search: string) {
    await this.page.goto(`/search?q=${search}`);
  }

  async getSongsCards() {
    return await this.project.resultsPage.songsCards.count()
  }

  async getArtistsCards() {
    return await this.project.resultsPage.artistCards.count()
  }

  async getFirstSongCard() {
    return this.project.resultsPage.songsCards.first()
  }

  async redirectSimilarSongs() {
    await this.project.resultsPage.similarSongsBtn.first().click()
  }

  async redirectSimilarArtists() {
    await this.project.resultsPage.similarArtistsBtn.first().click()
  }

  async getFirstArtistCard() {
    return this.project.resultsPage.artistCards.first()
  }

  async otherPlatformRedirection(platform: string) {
    if (platform === 'Spotify') {
      await this.project.resultsPage.songsCards.first().locator('.btn').first().click();
    }
  
    if (platform === 'YouTubeMusic') {
      await this.project.resultsPage.songsCards.first().locator('a:nth-child(2)').first().click();
    }
  
    if (platform === 'Deezer') {
      await this.project.resultsPage.songsCards.first().locator('a:nth-child(3)').first().click();
    }
  }

  async homeRedirect() {
    await this.project.resultsPage.homeBtn.click()
  }

}