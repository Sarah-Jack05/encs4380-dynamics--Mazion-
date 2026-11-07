 // 1. grab the 4 elements
      const kSlider = document.getElementById("k");
      const kOut = document.getElementById("k_out");
      const tSlider = document.getElementById("tau");
      const tOut = document.getElementById("tau_out");

      // 2. ONE function that does both jobs
      function update() {
        const k = Number(kSlider.value);
        const t = Number(tSlider.value);
        kOut.textContent = k;
        tOut.textContent = t;
      }

      // 3. run it when EITHER slider moves
      kSlider.addEventListener("input", update);
      tSlider.addEventListener("input", update);

      // 4. run it once at the start
      update();
