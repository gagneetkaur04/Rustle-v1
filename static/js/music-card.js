class MusicCard extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
  
      this.shadowRoot.innerHTML = `
        <style>
            .music-card {
                text-align: left;
                font-family: Arial, sans-serif;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                transition: 0.3s;
                width: 300px;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 10px;
            }
            
            .music-card .cover {
                width: 100%;
                height: auto;
                border-radius: 8px;
                margin-bottom: 10px;
                box-shadow: 2px #bbb;

            }
            
            .music-card  h2 {
                margin: 0;
            }
            
            .music-card audio {
                width: 100%;
                margin-top: 10px;
            }     
            .circular-button {
                width: 60px;
                height: 60px;
                background:#446868;
                border: none;
                border-radius: 50%;
                box-shadow: 2px 2px 5px #888888;
                font-size: 24px;
                color: #fff;
              }  
              .content-section {
                display: flex;
                align-items: center;
              }
              
              .song-info {
                flex: 1;
                padding-right: 20px;
              }         
        </style>

        <div class="music-card">
            <img src="${this.getAttribute('image')}" class="cover">
            <div class="content-section">
                <div class="song-info">
                    <h2>${this.getAttribute('title')}</h2>
                    <p>${this.getAttribute('artist')}</p>
                </div>
            <button type="button" class="circular-button" data-bs-toggle="modal" data-bs-target="#addToPlaylistModal">
                <img src="/static/images/playlist-add-1-32.png" alt=""> 
            </button>
            </div>
            <audio controls>
                <source src="${this.getAttribute('audio')}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
      `;
    }
  }
  
  customElements.define('music-card', MusicCard);
  