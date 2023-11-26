## MUSIC PLAYER

<footer class="footer clearfix">
    <div class="audioRail">
        <div class="audioRail_total">
            <div class="audioRail_buffered"></div>
            <div class="audioRail_current"></div>
            <button class="audioRail_dot"></button>
        </div>
    </div>

    <div class="audio_timeWrap">
        <time class="audio_currentTime">00:00</time>
        /
        <time class="audio_duration">00:00</time>
    </div>

    <article class="audioInfo">
        <div class="default default_album">
            <cite class="img"></cite>
        </div>

        <div class="audioText">
            <div>
                <a class="songName" href="javascript:;" data-srcPrefix="/songs/">We Must Groove ft. Burna Boy</a>
                <a class="lyricTo" href="javascript:;" title="View Lyrics"></a>
            </div>
            <a class="singerName" href="javascript:;" data-srcPrefix="/artists/">2baba - Warriors</a>
        </div>
    </article>

    <article class="audioControl">
        <button class="audio_playBtn audioUtils_btn_play"></button>
    </article>

    <article class="audioOperation">
        <button class="audioOperation_addPlaylist addPlaylist_event"></button>
    </article>

    <button class="audio_retract"></button>

    <article class="songList">
        <h2>Queue <cite class="count">(12)</cite>
            <button class="close"></button>
        </h2>
        <ol></ol>
    </article>
</footer>



## MUSIC PLAYER 2

<div class="o_item release">

<div class="pic">
<img src="/ai/89000/bundle.88115.thumb.small/pics.1.jpg?r=1674269802" title="I Love You So">
</div>
<div class="data_text">
<div class="artist">
<a href="/albums/?do=artist&amp;id=59296" title="Davina White" previewlistener="true">Davina White</a>
</div>
<div class="album_title"><i>I Love You So</i></div>
<div class="label color_green o1">
<a href="/albums/?do=label&amp;id=7047" title="Davina White" previewlistener="true">
Davina White
</a>&nbsp;-&nbsp;DAV160760</div>
</div>
<div class="track_text">
<div class="c_o" id="current_track">
<div><i>Davina White - <span class="color_grey">I Love You So (4:21)</span></i></div>
</div>
<script>
	playerMode = 'album';
	presetBundleId = 88115;
</script>
<div id="hap-wrapper" class="hap-epic" style="display: block;">
<div class="hap-player-outer" style="opacity: 1;">
<div class="hap-seekbar" id="waveform"><div class="hap-seekbar-wave hap-seekbar-wave-visible"><canvas width="652" height="50" class="hap-canvas-seekbar-bg"></canvas><div class="hap-seekbar-wave-progress" style="width: 73.5199%;"><canvas width="652" height="50" class="hap-canvas-seekbar-progress"></canvas></div></div><div class="hap-waveform-loader hap-waveform-loader-hidden" id="preparing"><div>Preparing...</div></div>
</div> 
<div class="hap-player-controls">  
<div class="hap-player-controls-left">  
<!--
<button type="button" class="hap-skip-backward hap-btn-reset hap-contr-btn" data-tooltip="Backward 10 seconds" data-skip-time="10">
<svg viewBox="0 0 16 16"><polygon points="1,8 8,14 8,8 8,2 "/><polygon points="15,2 8,8 15,14 "/></svg>
</button>-->
<button type="button" class="hap-prev-toggle hap-btn-reset hap-contr-btn" style="cursor: pointer;">
<svg viewBox="0 0 10.2 11.7"><polygon points="10.2,0 1.4,5.3 1.4,0 0,0 0,11.7 1.4,11.7 1.4,6.2 10.2,11.7"></polygon></svg>
</button>
<button type="button" class="hap-playback-toggle hap-btn-reset hap-contr-btn" style="cursor: pointer;">
<span class="hap-btn hap-btn-play" style="display: block;">
<svg viewBox="0 0 17.5 21.2"><path d="M0,0l17.5,10.9L0,21.2V0z"></path></svg>
</span>
<span class="hap-btn hap-btn-pause" style="display: none;">
<svg viewBox="0 0 17.5 21.2"><rect width="6" height="21.2"></rect><rect x="11.5" width="6" height="21.2"></rect></svg>
</span>
</button>
<button type="button" class="hap-next-toggle hap-btn-reset hap-contr-btn" style="cursor: pointer;">
<svg viewBox="0 0 10.2 11.7"><polygon points="0,11.7 8.8,6.4 8.8,11.7 10.2,11.7 10.2,0 8.8,0 8.8,5.6 0,0"></polygon></svg>
</button>
<!--
<button type="button" class="hap-skip-forward hap-btn-reset hap-contr-btn" data-tooltip="Forward 10 seconds" data-skip-time="10">
<svg viewBox="0 0 16 16"><polygon points="15,8 8,2 8,8 8,14 "/><polygon points="1,2 1,14 8,8 "/></svg>
</button>-->
<div class="hap-volume-wrap">
<button type="button" class="hap-volume-toggle hap-btn-reset hap-contr-btn hap-volume-toggable" data-tooltip="Volume">
<span class="hap-btn hap-btn-volume-up" style="display: block;">
<svg viewBox="0 0 48 48"><path d="M6 18v12h8l10 10V8L14 18H6zm27 6c0-3.53-2.04-6.58-5-8.05v16.11c2.96-1.48 5-4.53 5-8.06zM28 6.46v4.13c5.78 1.72 10 7.07 10 13.41s-4.22 11.69-10 13.41v4.13c8.01-1.82 14-8.97 14-17.54S36.01 8.28 28 6.46z"></path><path d="M0 0h48v48H0z" fill="none"></path></svg>
</span>
<span class="hap-btn hap-btn-volume-down" style="display: none;">
<svg viewBox="0 0 48 48"><path d="M37 24c0-3.53-2.04-6.58-5-8.05v16.11c2.96-1.48 5-4.53 5-8.06zm-27-6v12h8l10 10V8L18 18h-8z"></path><path d="M0 0h48v48H0z" fill="none"></path></svg>
</span>
<span class="hap-btn hap-btn-volume-off" style="display: none;">
<svg viewBox="0 0 48 48"><path d="M33 24c0-3.53-2.04-6.58-5-8.05v4.42l4.91 4.91c.06-.42.09-.85.09-1.28zm5 0c0 1.88-.41 3.65-1.08 5.28l3.03 3.03C41.25 29.82 42 27 42 24c0-8.56-5.99-15.72-14-17.54v4.13c5.78 1.72 10 7.07 10 13.41zM8.55 6L6 8.55 15.45 18H6v12h8l10 10V26.55l8.51 8.51c-1.34 1.03-2.85 1.86-4.51 2.36v4.13c2.75-.63 5.26-1.89 7.37-3.62L39.45 42 42 39.45l-18-18L8.55 6zM24 8l-4.18 4.18L24 16.36V8z"></path><path d="M0 0h48v48H0z" fill="none"></path></svg>
</span>
</button>
<div class="hap-volume-seekbar">
<div class="hap-volume-bg">
<div class="hap-volume-level" style="width: 101.6px;"></div>
</div>
</div>
</div>
</div>
<div class="hap-player-controls-right">
<button type="button" class="hap-loop-toggle hap-btn-reset hap-contr-btn" style="cursor: pointer;">
<span class="hap-btn hap-btn-loop-playlist hap-contr-btn-hover" data-tooltip="Loop playlist" style="display: block;">
<svg viewBox="0 0 512 512"><path d="M493.544 181.463c11.956 22.605 18.655 48.4 18.452 75.75C511.339 345.365 438.56 416 350.404 416H192v47.495c0 22.475-26.177 32.268-40.971 17.475l-80-80c-9.372-9.373-9.372-24.569 0-33.941l80-80C166.138 271.92 192 282.686 192 304v48h158.875c52.812 0 96.575-42.182 97.12-94.992.155-15.045-3.17-29.312-9.218-42.046-4.362-9.185-2.421-20.124 4.8-27.284 4.745-4.706 8.641-8.555 11.876-11.786 11.368-11.352 30.579-8.631 38.091 5.571zM64.005 254.992c.545-52.81 44.308-94.992 97.12-94.992H320v47.505c0 22.374 26.121 32.312 40.971 17.465l80-80c9.372-9.373 9.372-24.569 0-33.941l-80-80C346.014 16.077 320 26.256 320 48.545V96H161.596C73.44 96 .661 166.635.005 254.788c-.204 27.35 6.495 53.145 18.452 75.75 7.512 14.202 26.723 16.923 38.091 5.57 3.235-3.231 7.13-7.08 11.876-11.786 7.22-7.16 9.162-18.098 4.8-27.284-6.049-12.735-9.374-27.001-9.219-42.046z"></path></svg>
</span>
<span class="hap-btn hap-btn-loop-single hap-contr-btn-hover" data-tooltip="Loop single">
<svg viewBox="0 0 512 512"><path d="M493.544 181.463c11.956 22.605 18.655 48.4 18.452 75.75C511.339 345.365 438.56 416 350.404 416H192v47.495c0 22.475-26.177 32.268-40.971 17.475l-80-80c-9.372-9.373-9.372-24.569 0-33.941l80-80C166.138 271.92 192 282.686 192 304v48h158.875c52.812 0 96.575-42.182 97.12-94.992.155-15.045-3.17-29.312-9.218-42.046-4.362-9.185-2.421-20.124 4.8-27.284 4.745-4.706 8.641-8.555 11.876-11.786 11.368-11.352 30.579-8.631 38.091 5.571zM64.005 254.992c.545-52.81 44.308-94.992 97.12-94.992H320v47.505c0 22.374 26.121 32.312 40.971 17.465l80-80c9.372-9.373 9.372-24.569 0-33.941l-80-80C346.014 16.077 320 26.256 320 48.545V96H161.596C73.44 96 .661 166.635.005 254.788c-.204 27.35 6.495 53.145 18.452 75.75 7.512 14.202 26.723 16.923 38.091 5.57 3.235-3.231 7.13-7.08 11.876-11.786 7.22-7.16 9.162-18.098 4.8-27.284-6.049-12.735-9.374-27.001-9.219-42.046zm163.258 44.535c0-7.477 3.917-11.572 11.573-11.572h15.131v-39.878c0-5.163.534-10.503.534-10.503h-.356s-1.779 2.67-2.848 3.738c-4.451 4.273-10.504 4.451-15.666-1.068l-5.518-6.231c-5.342-5.341-4.984-11.216.534-16.379l21.72-19.939c4.449-4.095 8.366-5.697 14.42-5.697h12.105c7.656 0 11.749 3.916 11.749 11.572v84.384h15.488c7.655 0 11.572 4.094 11.572 11.572v8.901c0 7.477-3.917 11.572-11.572 11.572h-67.293c-7.656 0-11.573-4.095-11.573-11.572v-8.9z"></path></svg>
</span> 
<span class="hap-btn hap-btn-loop-off" data-tooltip="Loop off">
<svg viewBox="0 0 512 512"><path d="M493.544 181.463c11.956 22.605 18.655 48.4 18.452 75.75C511.339 345.365 438.56 416 350.404 416H192v47.495c0 22.475-26.177 32.268-40.971 17.475l-80-80c-9.372-9.373-9.372-24.569 0-33.941l80-80C166.138 271.92 192 282.686 192 304v48h158.875c52.812 0 96.575-42.182 97.12-94.992.155-15.045-3.17-29.312-9.218-42.046-4.362-9.185-2.421-20.124 4.8-27.284 4.745-4.706 8.641-8.555 11.876-11.786 11.368-11.352 30.579-8.631 38.091 5.571zM64.005 254.992c.545-52.81 44.308-94.992 97.12-94.992H320v47.505c0 22.374 26.121 32.312 40.971 17.465l80-80c9.372-9.373 9.372-24.569 0-33.941l-80-80C346.014 16.077 320 26.256 320 48.545V96H161.596C73.44 96 .661 166.635.005 254.788c-.204 27.35 6.495 53.145 18.452 75.75 7.512 14.202 26.723 16.923 38.091 5.57 3.235-3.231 7.13-7.08 11.876-11.786 7.22-7.16 9.162-18.098 4.8-27.284-6.049-12.735-9.374-27.001-9.219-42.046z"></path></svg>
</span>       
</button>
</div>
</div>
</div> 
<div class="hap-preloader" style="display: none;"></div>
</div>															




</div>
</div>


## LYRICS
```
I know you've been hard, I know that you're trying 
The bus is complaining, your phone's always ringing 
Outside there's the cold wind, inside the monotony 
Baby, we need an exit from this 
Honey, we need a squeeze release 
I know what we'll feel, the electric feelings 
You and me all night, yeah, 
I'll be alright If you close your eyes, close your eyes 
Feel the sunlight, baby, we'll fly 
To Madrid, wanna get away one night or two 
Madrid, go outside, look at me and you 
Fall in love one time, two times, three hundred times 
Wanna get far away, but I'm tired of the rainy days 
The heart that you warmed up, tell me you see it 
And I'll lose it in dancing, 
Spanish living Soon we'll be leaving, 
I'm so bad at feeling 
Baby, we need an exit from this 
Honey, we need a squeeze release 
Baby, we need an exit from this 
Honey, we need a squeeze release 
To Madrid, wanna get away one night or two 
Madrid, go outside, look at me and you 
Fall in love one time, two times, three hundred times 
Wanna get far away, but I'm tired of the rainy days 
To Madrid, wanna get away one night or two 
Madrid, go outside, look at me and you 
Fall in love one time, two times, three hundred times 
Wanna get far away, but I'm tired of the rainy days 
To Madrid, wanna get away one night or two 
Madrid, go outside, look at me and you 
Fall in love one time, two times, three hundred times 
Wanna get far away, but I'm tired of the rainy days 
To Madrid 
To Madrid 
To Madrid 
To Madrid
```


## SIDEBAR LIST
```html
    <li class="active">
        <a href="home_user.html"><i class="fas fa-headphones"></i> Discover</a>
    </li>
    <li>
        <a href="#"><i class="fas fa-music"></i> Genres</a>
    </li>
    <li>
        <a href="#"><i class="fas fa-user-friends"></i> Artists</a>
    </li>
    <li>
        <a href="user_profile.html"><i class="fas fa-list"></i> Playlists</a>
    </li>
    <li>
        <a href="#favorites"><i class="fas fa-heart"></i> Favorites</a>
    </li>
```