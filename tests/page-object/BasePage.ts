import {Locator, Page, expect} from "@playwright/test";


import {
  inizializeSongRecomender
} from "./locatorInitializationUtils";
import { songRecomenderProject } from "./interface";

export default class BasePage {

  readonly page: Page; 
  readonly project: songRecomenderProject

  constructor(page: Page) {
    this.page = page
    this.project = inizializeSongRecomender(page)

  }

  async navigateTo () {
    await this.page.goto('/')
  }

  async typeSearch (name: string) {
    await this.project.mainPage.findSongField.fill(name)
  }

  async findSong () {
    await this.project.mainPage.findSongBtn.click()
  }

  async spinWheel() {
    await this.project.mainPage.spinTheWheelBtn.click()
  }
  
  async getspinWheel() {
    return this.project.mainPage.spinTheWheelBtn
  }

  async searchGenre() {
    await this.project.mainPage.searchForGenre.click()
  }

  async getSearchGenreBtn() {
    return this.project.mainPage.searchForGenre
  }

  async musicalDefendersLink() {
    await this.project.mainPage.musicDefendersLink.click()
  }

  async noDataGoBack() {
    await this.project.noDataGoBack.click()
  }

}