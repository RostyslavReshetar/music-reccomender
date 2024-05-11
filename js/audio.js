// Variable to store the currently playing audio
let currentAudio = null;

// Function to format time
var timeString = (secs) => {
  let ss = Math.floor(secs),
    hh = Math.floor(ss / 3600),
    mm = Math.floor((ss - hh * 3600) / 60);
  ss = ss - hh * 3600 - mm * 60;

  if (hh > 0) {
    mm = mm < 10 ? "0" + mm : mm;
  }
  ss = ss < 10 ? "0" + ss : ss;
  return hh > 0 ? `${hh}:${mm}:${ss}` : `${mm}:${ss}`;
};

// Function to set progress
function setProgress(elTarget) {
  let divisionNumber = elTarget.getAttribute("max") / 100;
  let rangeNewWidth = Math.floor(elTarget.value / divisionNumber);
  if (rangeNewWidth > 95) {
    elTarget.nextSibling.style.width = "95%";
  } else {
    elTarget.nextSibling.style.width = rangeNewWidth + "%";
  }
}

// Iterate over all audio elements
for (let i of document.querySelectorAll(".aWrap")) {
  i.audio = new Audio(encodeURI(i.dataset.src));
  i.aPlay = i.querySelector(".aPlay");
  i.aPlayIco = i.querySelector(".aPlayIco");
  i.aNow = i.querySelector(".aNow");
  i.aTime = i.querySelector(".aTime");
  i.aSeek = i.querySelector(".aSeek");
  i.aVolume = i.querySelector(".aVolume");
  i.aVolIco = i.querySelector(".aVolIco");
  i.seeking = false;

  i.aPlay.onclick = () => {
    if (i.audio.paused) {
      if (currentAudio && currentAudio !== i.audio) {
        currentAudio.pause();
      }
      i.audio.play();
      currentAudio = i.audio;
    } else {
      i.audio.pause();
    }
  };

  i.audio.onplay = () => (i.aPlayIco.innerHTML = '<i class="fa fa-pause"></i>');
  i.audio.onpause = () => (i.aPlayIco.innerHTML = '<i class="fa fa-play"></i>');

  i.audio.onloadstart = () => {
    i.aNow.innerHTML = "Loading";
    i.aTime.innerHTML = "";
  };

  i.audio.onloadedmetadata = () => {
    i.aNow.innerHTML = timeString(0);
    i.aTime.innerHTML = timeString(i.audio.duration);
    i.aSeek.max = Math.floor(i.audio.duration);

    i.aSeek.oninput = () => (i.seeking = true);
    i.aSeek.onchange = () => {
      i.audio.currentTime = i.aSeek.value;
      if (!i.audio.paused) {
        i.audio.play();
      }
      i.seeking = false;
    };

    i.audio.ontimeupdate = () => {
      if (!i.seeking) {
        i.aSeek.value = Math.floor(i.audio.currentTime);
      }
      i.aNow.innerHTML = timeString(i.audio.currentTime);
      let divisionNumber = i.aSeek.getAttribute("max") / 100;
      let rangeNewWidth = Math.floor(i.aSeek.value / divisionNumber);
      if (rangeNewWidth > 95) {
        i.aSeek.nextSibling.style.width = "95%";
      } else {
        i.aSeek.nextSibling.style.width = rangeNewWidth + "%";
      }
    };
  };

  i.aVolIco.onclick = () => {
    i.audio.volume = i.audio.volume == 0 ? 1 : 0;
    i.aVolume.value = i.audio.volume;
    i.aVolIco.innerHTML =
      i.aVolume.value == 0
        ? '<i class="fa fa-volume-off"></i>'
        : '<i class="fa fa-volume-up"></i>';
    if (i.aVolume.value == 0) {
      i.aVolume.nextSibling.style.width = "0%";
    } else {
      i.aVolume.nextSibling.style.width = "95%";
    }
  };
  i.aVolume.onchange = () => {
    i.audio.volume = i.aVolume.value;
    i.aVolIco.innerHTML =
      i.aVolume.value == 0
        ? '<i class="fa fa-volume-off"></i>'
        : '<i class="fa fa-volume-up"></i>';
  };

  i.audio.oncanplaythrough = () => {
    i.aPlay.disabled = false;
    i.aVolume.disabled = false;
    i.aSeek.disabled = false;
  };
  i.audio.onwaiting = () => {
    i.aPlay.disabled = true;
    i.aVolume.disabled = true;
    i.aSeek.disabled = true;
  };

  i.aSeek.addEventListener("input", function () {
    setProgress(this);
  });

  i.aVolume.addEventListener("input", function () {
    setProgress(this);
  });
}
