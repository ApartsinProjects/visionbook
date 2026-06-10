/**
 * Book interactivity: collapsible code blocks, exercises, labs, bibliography, and answers.
 * Loaded by all section HTML files via <script defer src="...scripts/book.js">.
 */
document.addEventListener('DOMContentLoaded', function () {

  // 1. Make ALL <pre> code blocks collapsible.
  //    - Code AND its sibling .code-output go inside a <details> element
  //      so that when "Show code" is closed, BOTH code and output hide
  //      (per editorial decision: an output without its code is noise)
  //    - .code-caption stays visible as a figure label
  //    - Short code blocks (10 lines or fewer) start OPEN
  //    - Longer code blocks start COLLAPSED
  //    - SKIP pre elements inside library-shortcut callouts; step 9c
  //      handles those with its own outer "Show code" wrapper (avoids
  //      the "show code in show code" double-wrap reported in 42.1)
  document.querySelectorAll('pre').forEach(function (pre) {
    // Skip if already inside a <details> element
    if (pre.closest('details')) return;
    // Skip if inside a callout UNLESS it's wrapped in a code-block-wrapper
    if (pre.closest('.callout') && !pre.closest('.code-block-wrapper')) return;
    // Skip if inside a library-shortcut: step 9c handles those
    if (pre.closest('.callout.library-shortcut')) return;
    // Skip inline-style pre (very short, less than 20 chars)
    var text = pre.textContent || '';
    if (text.trim().length < 20) return;

    // Count lines
    var lines = text.split('\n');
    var lineCount = lines.length;
    // Trim trailing empty lines
    while (lineCount > 0 && lines[lineCount - 1].trim() === '') lineCount--;

    var isShort = lineCount <= 10;

    // Create the <details> wrapper for code (+ output)
    var details = document.createElement('details');
    details.className = 'code-collapse';
    if (isShort) {
      details.setAttribute('open', '');
    }

    var summary = document.createElement('summary');
    var icon = document.createElement('img');
    var cssLink = document.querySelector('link[rel="stylesheet"][href*="book.css"]');
    icon.src = cssLink ? cssLink.href.replace('book.css', 'icons/callout-code.svg') : '../../styles/icons/callout-code.svg';
    icon.alt = '';
    icon.className = 'code-collapse-icon';
    summary.appendChild(icon);
    summary.appendChild(document.createTextNode(isShort ? 'Code (' + lineCount + ' lines)' : 'Show Code (' + lineCount + ' lines)'));
    details.appendChild(summary);

    // Insert details before the pre, then move pre inside
    pre.parentNode.insertBefore(details, pre);
    details.appendChild(pre);

    // Move the immediately-following <div class="code-output"> inside the
    // same details so it hides together with the code. Stops at the first
    // non-whitespace non-code-output sibling (typically the caption).
    var cursor = details.nextSibling;
    while (cursor) {
      if (cursor.nodeType === 3 && (cursor.textContent || '').trim() === '') {
        // whitespace text node: skip and continue scanning
        cursor = cursor.nextSibling;
        continue;
      }
      if (cursor.nodeType === 1) {
        var cls = cursor.className || '';
        if (typeof cls === 'string' && cls.indexOf('code-output') >= 0) {
          var moved = cursor;
          cursor = cursor.nextSibling;
          details.appendChild(moved);
          continue;
        }
      }
      break;
    }
  });

  // 2. Remove standalone "Exercises" headings (redundant with the container title).
  //    Matches: "Exercises", "8. Exercises", "Section 8: Exercises", etc.
  document.querySelectorAll('h2').forEach(function (h2) {
    var text = h2.textContent.trim();
    if (/^(?:\d+\.\s*)?Exercises$/i.test(text) || /^Section\s+\d+[.:]\s*Exercises$/i.test(text)) {
      h2.remove();
    }
  });

  // 2b. Remove "Hands-On Lab" exercise callouts (redundant with collapsible lab).
  document.querySelectorAll('.callout.exercise').forEach(function (ex) {
    var title = ex.querySelector('.callout-title');
    if (title && title.textContent.trim() === 'Hands-On Lab') {
      ex.remove();
    }
  });

  // 3. Reposition elements before .whats-next in correct order:
  //    ... content ... [lab] [self-check] [exercises] [whats-next] ...
  var whatsNext = document.querySelector('.whats-next');

  if (whatsNext) {
    // Move all exercises to just before .whats-next
    var allExercises = document.querySelectorAll('.callout.exercise');
    allExercises.forEach(function (ex) {
      whatsNext.parentNode.insertBefore(ex, whatsNext);
    });

    // Move self-check to just before the first exercise (or before .whats-next if no exercises)
    var selfCheck = document.querySelector('.callout.self-check');
    if (selfCheck) {
      var firstExercise = document.querySelector('.callout.exercise');
      var target = firstExercise || whatsNext;
      target.parentNode.insertBefore(selfCheck, target);
    }

    // Move labs to just before self-check, exercises, or .whats-next
    // (runs before collapsible wrapping, so move raw elements)
    document.querySelectorAll('.lab').forEach(function (lab) {
      // Also grab the h3.lab-title if it precedes the lab
      var prev = lab.previousElementSibling;
      var labTitleEl = (prev && prev.classList && prev.classList.contains('lab-title')) ? prev : null;

      var target = document.querySelector('.callout.self-check') ||
                   document.querySelector('.callout.exercise') ||
                   whatsNext;

      if (target) {
        if (labTitleEl) target.parentNode.insertBefore(labTitleEl, target);
        target.parentNode.insertBefore(lab, target);
      }
    });
  }

  // 4. Merge all consecutive .callout.exercise into a single collapsible container
  var exercises = document.querySelectorAll('.callout.exercise');
  var processed = new Set();

  exercises.forEach(function (ex) {
    if (processed.has(ex)) return;

    // Collect the run of consecutive .callout.exercise siblings
    var group = [ex];
    processed.add(ex);
    var next = ex.nextElementSibling;
    while (next && next.classList.contains('callout') && next.classList.contains('exercise')) {
      group.push(next);
      processed.add(next);
      next = next.nextElementSibling;
    }

    var count = group.length;

    // Create wrapper <details> (collapsed by default)
    var wrapper = document.createElement('details');
    wrapper.className = 'exercises-container';

    var summary = document.createElement('summary');
    summary.className = 'exercises-summary';
    summary.innerHTML = '<span class="exercises-icon">&#9998;</span> Exercises (' + count + ')';
    wrapper.appendChild(summary);

    // Insert wrapper before the first exercise
    group[0].parentNode.insertBefore(wrapper, group[0]);

    // Move all exercises into the wrapper
    group.forEach(function (el) {
      el.classList.add('exercise-inside-group');
      // Ensure individual exercise answers are collapsed
      el.querySelectorAll('details[open]').forEach(function (d) {
        d.removeAttribute('open');
      });
      wrapper.appendChild(el);
    });
  });

  // 5. Make self-check collapsible and collapsed by default.
  document.querySelectorAll('.callout.self-check').forEach(function (sc) {
    // Skip if already wrapped
    if (sc.closest('details.selfcheck-collapse')) return;

    var titleEl = sc.querySelector('.callout-title');
    var scTitle = titleEl ? titleEl.textContent.trim() : 'Self-Check';

    var details = document.createElement('details');
    details.className = 'selfcheck-collapse';

    var summary = document.createElement('summary');
    summary.className = 'selfcheck-collapse-summary';
    summary.innerHTML = '<span class="selfcheck-collapse-icon">&#9745;</span> ' + scTitle;
    details.appendChild(summary);

    // Remove the callout-title since it is in the summary now
    if (titleEl) titleEl.remove();

    sc.parentNode.insertBefore(details, sc);
    details.appendChild(sc);

    // Collapse individual answers inside
    sc.querySelectorAll('details[open]').forEach(function (d) {
      d.removeAttribute('open');
    });
  });

  // 6. Make labs collapsible and collapsed by default.
  //    Priority order for the lab title:
  //      1. <div class="callout-title"> inside the lab (CANONICAL form)
  //      2. <h3 class="lab-title"> immediately before the lab (legacy)
  //      3. First <h2>/<h3> inside the lab div (legacy)
  //      4. Fallback "Hands-On Lab"
  //
  //    Match only <div class="callout lab"> / <div class="lab"> tops, NOT
  //    inner divs like .lab-objective, .lab-meta, .lab-skills (those match
  //    `class="lab-objective"` etc. which the `.lab` selector already skips
  //    because class names are whole tokens). The previous version of this
  //    routine ignored the canonical .callout-title and instead picked up the
  //    "Objective" h3 inside .lab-objective as the lab title, producing two
  //    misleading rendered cards: "Hands-On Lab" (fallback) and
  //    "Lab: Objective" (mis-identified). Now we prioritize .callout-title.
  document.querySelectorAll('.lab').forEach(function (lab) {
    // Skip if already inside a details
    if (lab.closest('details.lab-collapse')) return;

    var titleEl = lab.previousElementSibling;
    var labTitle = 'Hands-On Lab';
    var removeInternalHeading = false;
    var internalHeading = null;
    var calloutTitleEl = null;

    // PRIORITY 1: canonical callout-title inside the lab (direct child only,
    // not any descendant — to avoid grabbing a step-level callout-title).
    for (var i = 0; i < lab.children.length; i++) {
      var ch = lab.children[i];
      if (ch.classList && ch.classList.contains('callout-title')) {
        calloutTitleEl = ch;
        break;
      }
    }
    if (calloutTitleEl) {
      labTitle = calloutTitleEl.textContent.trim();
      // Normalize "Hands-On Lab: X" → "Lab: X" for visual consistency
      labTitle = labTitle.replace(/^Hands-On Lab:\s*/i, 'Lab: ');
    } else if (titleEl && titleEl.classList.contains('lab-title')) {
      // PRIORITY 2: legacy <h3 class="lab-title">Lab: ...</h3> before the lab
      labTitle = titleEl.textContent.trim();
    } else {
      // PRIORITY 3: first h2/h3 inside the lab div
      internalHeading = lab.querySelector('h2, h3');
      if (internalHeading) {
        var headingText = internalHeading.textContent.trim();
        labTitle = headingText.replace(/^Hands-On Lab:\s*/i, 'Lab: ');
        if (labTitle === headingText && !headingText.toLowerCase().startsWith('lab')) {
          labTitle = 'Lab: ' + headingText;
        }
        removeInternalHeading = true;
      }
    }

    // Create <details> wrapper (collapsed by default)
    var details = document.createElement('details');
    details.className = 'lab-collapse';

    var summary = document.createElement('summary');
    summary.className = 'lab-collapse-summary';
    summary.innerHTML = '<span class="lab-collapse-icon">&#128736;</span> ' + labTitle;
    details.appendChild(summary);

    var insertBefore = (titleEl && titleEl.classList.contains('lab-title')) ? titleEl : lab;
    insertBefore.parentNode.insertBefore(details, insertBefore);

    if (titleEl && titleEl.classList.contains('lab-title')) {
      details.appendChild(titleEl);
    }
    // Remove the canonical .callout-title element from the lab body since it
    // is now in the collapsible summary (avoids visual duplication).
    if (calloutTitleEl) {
      calloutTitleEl.remove();
    }
    // Remove internal heading since title is now in the collapsible summary
    if (removeInternalHeading && internalHeading) {
      internalHeading.remove();
    }
    details.appendChild(lab);
  });

  // 7. Make code output collapsible and collapsed by default. Skip:
  //  - outputs already inside a details (idempotency)
  //  - outputs inside a library-shortcut callout (the entire shortcut
  //    already collapses via step 9c, so a NESTED "Show output" toggle
  //    looks like double-collapse / "show code in show code")
  //  - very short outputs (<= 6 lines) where the toggle has no value
  document.querySelectorAll('.code-output').forEach(function (out) {
    if (out.closest('details.output-collapse')) return;
    if (out.closest('.callout.library-shortcut')) return;

    var lines = (out.textContent || '').split('\n');
    var lineCount = lines.length;
    while (lineCount > 0 && lines[lineCount - 1].trim() === '') lineCount--;
    if (lineCount <= 6) return;

    var details = document.createElement('details');
    details.className = 'output-collapse';

    var summary = document.createElement('summary');
    summary.className = 'output-collapse-summary';
    summary.textContent = 'Output (' + lineCount + ' lines)';
    details.appendChild(summary);

    out.parentNode.insertBefore(details, out);
    details.appendChild(out);
  });

  // 8. Make bibliography/references collapsible and collapsed by default.
  document.querySelectorAll('section.bibliography').forEach(function (bib) {
    // Skip if already inside any bibliography collapsible wrapper (either
    // the JS-injected `.bib-collapse` from a prior run, OR the canonical
    // server-side `<details class="bibliography-collapsible">` wrapper).
    // The canonical wrapper provides its own `<summary>Further Reading</summary>`
    // so a second JS-wrap would render "Further Reading" + the nested
    // "References and Further Reading" header (the "double bibliography
    // header" bug reported in section-27.1).
    if (bib.closest('details.bib-collapse')) return;
    if (bib.closest('details.bibliography-collapsible')) return;

    // Find the heading: h2, h3, or .bibliography-title div. Book HTML uses
    // <h3>Bibliography and Further Reading</h3>; an earlier version only
    // queried for h2, so the heading-removal below silently did nothing and
    // every section rendered the summary AND the h3 (the "double bibliography
    // header" bug).
    var heading = bib.querySelector('h2') ||
                  bib.querySelector('h3') ||
                  bib.querySelector('.bibliography-title');
    var bibTitle = heading ? heading.textContent.trim() : 'References and Further Reading';

    var details = document.createElement('details');
    details.className = 'bib-collapse';

    var summary = document.createElement('summary');
    summary.className = 'bib-collapse-summary';
    summary.innerHTML = '<span class="bib-collapse-icon">&#128218;</span> ' + bibTitle;
    details.appendChild(summary);

    // Remove the heading since we have it in the summary
    if (heading) heading.remove();

    bib.parentNode.insertBefore(details, bib);
    details.appendChild(bib);
  });

  // 9. Make practical-example callouts collapsible and collapsed by default.
  document.querySelectorAll('.callout.practical-example').forEach(function (pe) {
    if (pe.closest('details.scenario-collapse')) return;

    var titleEl = pe.querySelector('.callout-title');
    var peTitle = titleEl ? titleEl.textContent.trim() : 'Real-World Scenario';

    // Split title into prefix ("Real-World Scenario:") and topic
    var prefix = 'Real-World Scenario';
    var topic = '';
    var colonIdx = peTitle.indexOf(':');
    if (colonIdx > 0 && peTitle.substring(0, colonIdx).trim().indexOf('Scenario') >= 0) {
      prefix = peTitle.substring(0, colonIdx).trim();
      topic = peTitle.substring(colonIdx + 1).trim();
    } else if (peTitle !== 'Real-World Scenario') {
      topic = peTitle;
    }

    var details = document.createElement('details');
    details.className = 'scenario-collapse';

    var summary = document.createElement('summary');
    summary.className = 'scenario-collapse-summary';
    var label = '<span class="scenario-collapse-icon">&#127758;</span> <strong>' + prefix + '</strong>';
    if (topic) label += ': ' + topic;
    summary.innerHTML = label;
    details.appendChild(summary);

    if (titleEl) titleEl.remove();

    pe.parentNode.insertBefore(details, pe);
    details.appendChild(pe);
  });

  // 9b. Make research-frontier callouts collapsible and collapsed by default.
  //     The frontier discussion is long-form open-questions content that
  //     reads as an aside; collapsing keeps the section header-line clean.
  document.querySelectorAll('.callout.research-frontier').forEach(function (rf) {
    if (rf.closest('details.frontier-collapse')) return;

    var titleEl = rf.querySelector('.callout-title');
    var rfTitle = titleEl ? titleEl.textContent.trim() : 'Research Frontier';

    var prefix = 'Research Frontier';
    var topic = '';
    var colonIdx = rfTitle.indexOf(':');
    if (colonIdx > 0) {
      prefix = rfTitle.substring(0, colonIdx).trim();
      topic = rfTitle.substring(colonIdx + 1).trim();
    } else if (rfTitle !== 'Research Frontier') {
      topic = rfTitle;
    }

    var details = document.createElement('details');
    details.className = 'frontier-collapse';

    var summary = document.createElement('summary');
    summary.className = 'frontier-collapse-summary';
    var label = '<span class="frontier-collapse-icon">&#128300;</span> <strong>' + prefix + '</strong>';
    if (topic) label += ': ' + topic;
    summary.innerHTML = label;
    details.appendChild(summary);

    if (titleEl) titleEl.remove();

    rf.parentNode.insertBefore(details, rf);
    details.appendChild(rf);
  });

  // 9c. Make library-shortcut callouts' code blocks collapsible.
  //     The code is reference material the reader looks up when they need
  //     it; collapsing keeps the running prose compact. ONLY the inner
  //     code blocks collapse; the prose "pip install" line and the
  //     library-shortcut title stay visible.
  //
  //     Edge case (fixed 2026-05-18): some library-shortcuts contain
  //     MULTIPLE code-block-wrappers. The earlier logic wrapped only
  //     the first, leaving the second visible (visually "show code +
  //     another code block"). We now wrap ALL code-block-wrappers
  //     inside the library-shortcut together, in a single details that
  //     spans from the first wrapper to the last sibling that is still
  //     code-related (subsequent code-block-wrappers).
  document.querySelectorAll('.callout.library-shortcut').forEach(function (ls) {
    // Self-heal: previous book.js versions could add a redundant nested
    // <details class="shortcut-code-collapse"> inside an existing
    // <details class="code-collapsible">, producing TWO "Show code" buttons.
    // If we detect that nested-pair state, unwrap the inner shortcut wrapper.
    var existingCollapsible = ls.querySelector('details.code-collapsible');
    if (existingCollapsible) {
      var innerDup = existingCollapsible.querySelector('details.shortcut-code-collapse');
      if (innerDup) {
        var parent = innerDup.parentNode;
        Array.prototype.slice.call(innerDup.childNodes).forEach(function (node) {
          if (node.tagName !== 'SUMMARY') {
            parent.insertBefore(node, innerDup);
          }
        });
        innerDup.remove();
      }
      // Either way, don't add a new outer wrapper if collapsible already exists.
      return;
    }
    // Skip if we've already wrapped at the top level (idempotency).
    if (ls.querySelector('details.shortcut-code-collapse')) return;
    var firstCb = ls.querySelector('.code-block-wrapper');
    if (!firstCb) return;

    // Collect all code-block-wrappers in document order inside this shortcut
    var blocks = Array.prototype.slice.call(
      ls.querySelectorAll('.code-block-wrapper')
    );
    if (blocks.length === 0) return;

    var details = document.createElement('details');
    details.className = 'shortcut-code-collapse';

    var summary = document.createElement('summary');
    summary.className = 'shortcut-code-collapse-summary';
    var label = blocks.length === 1
      ? '<span class="shortcut-code-icon">&#9881;</span> Show code'
      : '<span class="shortcut-code-icon">&#9881;</span> Show code (' + blocks.length + ' blocks)';
    summary.innerHTML = label;
    details.appendChild(summary);

    // Insert details before the first code block, then move all blocks into it
    firstCb.parentNode.insertBefore(details, firstCb);
    blocks.forEach(function (cb) {
      details.appendChild(cb);
    });
  });

  // 10. Google-like search results (v6.37): Pagefind UI prefixes each result
  //     title with "[Part X › Ch Y]  Real Title" because we cannot inject HTML
  //     into result.meta.title (Pagefind UI escapes it). After Pagefind renders
  //     a result, lift the prefix out of the link text and into a separate
  //     <span class="pf-breadcrumb"> placed BEFORE the title — like Google's
  //     URL/breadcrumb path above the page title.
  function liftBreadcrumbs(root) {
    var links = root.querySelectorAll('.pagefind-ui__result-link');
    links.forEach(function (a) {
      if (a.dataset.pfBcDone) return;
      var text = a.textContent || '';
      var m = text.match(/^\[([^\]]+)\]\s+(.+)$/);
      if (!m) { a.dataset.pfBcDone = '1'; return; }
      var crumb = m[1];
      var title = m[2];
      // Title may already contain Pagefind <mark> highlights — preserve them
      // by using the link's existing innerHTML and stripping the prefix.
      var html = a.innerHTML;
      var prefixEnd = html.indexOf(']');
      if (prefixEnd !== -1) {
        // Remove "[crumb]  " prefix from the link's HTML (preserves <mark>)
        html = html.slice(prefixEnd + 1).replace(/^\s+/, '');
        a.innerHTML = html;
      }
      // Insert a small breadcrumb element BEFORE the link's parent <p>
      var titleP = a.closest('p, .pagefind-ui__result-title') || a.parentNode;
      var bc = document.createElement('div');
      bc.className = 'pf-breadcrumb';
      bc.textContent = crumb;
      titleP.parentNode.insertBefore(bc, titleP);
      a.dataset.pfBcDone = '1';
    });
  }
  // Watch the search container for new results
  var searchEl = document.getElementById('search');
  if (searchEl && window.MutationObserver) {
    var mo = new MutationObserver(function (mutations) {
      liftBreadcrumbs(searchEl);
    });
    mo.observe(searchEl, { childList: true, subtree: true });
  }

  // Wave D6 search-icon UX: click to open, ESC or click-outside to close.
  // The .header-search wrapper has CSS that hides the search card by
  // default and reveals it when .search-open is set. We toggle the class
  // on click, focus the input on open, and bind ESC + outside-click to
  // close.
  // Initialize PagefindUI on the header-search target if pagefind-ui.js
  // has loaded. Without this, section/index pages show an empty
  // <div id="search"> with no input. toc.html and the home index already
  // have their own inline initializer; this is the catch-all for every
  // other page that includes the header-search element.
  var searchTarget = document.getElementById('search');
  // When opened directly from disk via file://, browsers block pagefind's
  // fetch() calls for the index files (cross-origin policy on local files).
  // Detect that case and render a friendly message instead of an empty box.
  if (searchTarget && location.protocol === 'file:'
      && !searchTarget.dataset.pfInitialized) {
    searchTarget.innerHTML =
      '<div class="search-offline-note">'
      + '<strong>Search needs a local web server.</strong><br>'
      + 'Run <code>python -m http.server 8765</code> from the book folder, '
      + 'then open <code>http://localhost:8765/toc.html</code>.'
      + '</div>';
    searchTarget.dataset.pfInitialized = 'offline';
  }
  if (searchTarget && window.PagefindUI && !searchTarget.dataset.pfInitialized) {
    try {
      new PagefindUI({
        element: '#search',
        showSubResults: true,
        showImages: false,
        resetStyles: false,
        pageSize: 8,
        autofocus: false,
        translations: { placeholder: 'Search the book…' },
        processResult: function (result) {
          try {
            var part = (result && result.meta && result.meta.part)
              ? result.meta.part : '';
            var chap = (result && result.meta && result.meta.chapter)
              ? result.meta.chapter : '';
            var partShort = part.split(':')[0].trim();
            var chapShort = chap.split(':')[0].trim();
            var crumb = [partShort, chapShort].filter(Boolean).join(' › ');
            if (crumb && result.meta && result.meta.title
                && result.meta.title.indexOf('[' + partShort) !== 0) {
              result.meta.title = '[' + crumb + ']  ' + result.meta.title;
            }
          } catch (e) { /* fall through */ }
          return result;
        },
      });
      searchTarget.dataset.pfInitialized = '1';
    } catch (err) {
      // pagefind-ui.js failed to load; nothing to do.
    }
  }

  var searchWrap = document.querySelector('.header-search');
  if (searchWrap) {
    searchWrap.setAttribute('role', 'button');
    searchWrap.setAttribute('tabindex', '0');
    searchWrap.setAttribute('aria-label', 'Search the book');
    var openSearch = function () {
      if (searchWrap.classList.contains('search-open')) return;
      searchWrap.classList.add('search-open');
      searchWrap.setAttribute('aria-expanded', 'true');
      setTimeout(function () {
        var input = searchWrap.querySelector('input[type="text"], .pagefind-ui__search-input');
        if (input) input.focus();
      }, 50);
    };
    var closeSearch = function () {
      searchWrap.classList.remove('search-open');
      searchWrap.setAttribute('aria-expanded', 'false');
    };
    searchWrap.addEventListener('click', function (e) {
      if (e.target === searchWrap) {
        e.stopPropagation();
        if (searchWrap.classList.contains('search-open')) closeSearch();
        else openSearch();
      }
    });
    searchWrap.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && e.target === searchWrap) {
        e.preventDefault();
        openSearch();
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && searchWrap.classList.contains('search-open')) {
        closeSearch();
        searchWrap.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (!searchWrap.contains(e.target) &&
          searchWrap.classList.contains('search-open')) {
        closeSearch();
      }
    });
  }
});
