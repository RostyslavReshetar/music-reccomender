import {Locator} from "@playwright/test";


export interface songRecomenderProject {

  mainPage: {
    findSongField: Locator
    findSongBtn: Locator

    spinTheWheelBtn: Locator
    searchForGenre: Locator

    musicDefendersLink: Locator
  }

  noDataGoBack: Locator

  resultsPage: {
    songsCards: Locator
    artistCards: Locator

    similarSongsBtn: Locator
    similarArtistsBtn: Locator

    homeBtn: Locator

      //artistName: Locator
      //songName: Locator
      //playSongBtn: Locator
  
      //spotifyBtn: Locator
      //youTubeMusicBtn: Locator
      //deezerBtn: Locator
      
      //similarSongBtn: Locator
      //similarArtistBtn: Locator
      
      //returnHome: Locator

  }


}