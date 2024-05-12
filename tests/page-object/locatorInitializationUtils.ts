import {Locator, Page} from "@playwright/test";

export function inizializeSongRecomender (page :Page) {
  return {
    mainPage: {
      findSongField: page.getByPlaceholder('Enter song name'),
      findSongBtn: page.getByRole('button').first(),
  
      spinTheWheelBtn: page.getByRole('button', { name: 'Spin the wheel' }),
      searchForGenre: page.locator('#searchButton'),
  
      musicDefendersLink: page.getByRole('link', { name: 'https://' }),
    },
  
    noDataGoBack: page.getByRole('link', { name: 'Go Back' }),

    resultsPage: {
      songsCards: page.locator('[test-data="songs-card"] > div'),
      artistCards: page.locator('[test-data="artits-card"] > div'),

      similarSongsBtn: page.locator(`a:has-text("Similar Songs")`),
      similarArtistsBtn: page.locator(`a:has-text("Similar Artists")`),

      homeBtn: page.getByRole('link', { name: 'Return Home' }),
  
  
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
}