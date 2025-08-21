// assets/animate_stats.js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
  stats: {
    animate: function(targets) {
      if (!targets) {
        return window.dash_clientside.no_update;
      }

      function fmt(n) {
        try { return Number(n).toLocaleString('en-GB'); } catch (e) { return n; }
      }
      function animText(elId, target) {
        const el = document.getElementById(elId);
        if (!el) return null;
        const start = parseInt(el.getAttribute('data-value') || '0', 10);
        const end = parseInt(target || 0, 10);
        if (start === end) {
          el.textContent = fmt(end);
          el.setAttribute('data-value', end);
          return null;
        }
        const dur = 600;
        const t0 = performance.now();
        function step(t) {
          const p = Math.min(1, (t - t0) / dur);
          const eased = 1 - Math.pow(1 - p, 3);
          const val = Math.round(start + (end - start) * eased);
          el.textContent = fmt(val);
          el.setAttribute('data-value', val);
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        return null;
      }

      // Regions label/suffix (no animation)
      const labelEl = document.getElementById('stat-regions-label');
      const suffixEl = document.getElementById('stat-regions-suffix');
      if (labelEl) labelEl.textContent = targets.regions_label || '';
      if (suffixEl) suffixEl.textContent = targets.regions_suffix || '';

      // Animated numbers
      animText('stat-icbs-value', targets.icbs_value);
      animText('stat-providers-value', targets.providers_value);

      return null; // sink output
    }
  }
});
