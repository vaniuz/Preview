(function(){
  'use strict';

  // Depoimentos reais — Google Maps (5,0 · 19 avaliações), texto integral do paciente.
  var testimonials = [
    {
      quote: "Excelente experiência na LAVIC Odontologia! Fui muito bem atendida desde o primeiro contato. A Gabrielly foi extremamente atenciosa e prestativa, me auxiliando em todo o processo, desde o agendamento até o suporte com as autorizações do convênio. O Dr. Matheus também merece destaque pela atenção, profissionalismo e cuidado durante o atendimento. Realizou minha avaliação e limpeza com muita dedicação, além de explicar tudo de forma clara, honesta e transparente. A Dra. Izabelly igualmente foi muito atenciosa e prestativa durante todo o atendimento. Super recomendo a equipe e a clínica LAVIC Odontologia pela excelência no atendimento e cuidado com os pacientes",
      author: "Fernanda Comunale",
      role: "1 avaliação",
      company: "há 3 meses · Avaliação Google",
      avatar: "F"
    },
    {
      quote: "O Dr Matheus me atendeu gentilmente, me explicou tudo o que precisa fazer com toda paciência e transparência, o que me deixou certa de que escolhi o melhor lugar pra tratar o sorriso. Quero deixar aqui o meu agradecimento e a minha satisfação!",
      author: "Mateus Oliveira",
      role: "1 avaliação",
      company: "há 3 meses · Avaliação Google",
      avatar: "M"
    },
    {
      quote: "Já fiz restauração e extração, foi ótima minha experiência. Só faço limpeza com a Dra Ana agora!! Recomendo muito!! Super atenciosos.",
      author: "Tassiany Oliveira",
      role: "2 avaliações",
      company: "há 4 meses · Avaliação Google",
      avatar: "T"
    },
    {
      quote: "Fiz limpeza e clareamento na LAVIC Odontologia com a Dra. Izabelly e fui muito bem atendido. O atendimento foi super tranquilo, ela explica tudo direitinho e deixa a gente bem à vontade durante o procedimento. A limpeza ficou ótima e o clareamento deu uma diferença bem visível. Curti muito o resultado e também o cuidado da equipe. Recomendo demais a clínica e o trabalho da doutora!",
      author: "Geraldo Paiva",
      role: "5 avaliações",
      company: "há 6 meses · Avaliação Google",
      avatar: "G"
    },
    {
      quote: "Doutores ótimos!!! Muito atenciosos e super calmos para explicarem sobre os procedimentos. Me senti muito segura durante o atendimento. Recomendo de olhos fechados!!!!",
      author: "Lauriette Matos",
      role: "1 avaliação",
      company: "há 6 meses · Avaliação Google",
      avatar: "L"
    }
  ];

  var tActive = 0;
  var tTransitioning = false;

  function initTestimonials(){
    window.moveTestimonial = moveTestimonial;
  }

  function goToTestimonial(idx){
    if(tTransitioning || idx === tActive) return;
    tActive = idx;
    renderTestimonial(idx);
    tTransitioning = true;
    setTimeout(function(){ tTransitioning = false; }, 400);
  }

  function renderTestimonial(idx){
    var t = testimonials[idx];
    var quoteEl = document.getElementById("tQuote");
    var authorEl = document.getElementById("tName");
    var roleEl = document.getElementById("tRole");
    var metaEl = document.getElementById("tMeta");
    var avatarEl = document.getElementById("tAvatar");
    var indexEl = document.getElementById("tIndex");
    var counterEl = document.getElementById("tCounter");
    var linesEl = document.getElementById("tLines");
    var authorWrap = document.getElementById("tAuthor");

    if(!quoteEl) return;

    quoteEl.classList.add("fade");
    authorWrap.classList.add("fade");

    setTimeout(function(){
      quoteEl.textContent = t.quote;
      authorEl.textContent = t.author;
      roleEl.textContent = t.role;
      metaEl.textContent = t.company;
      if(t.avatarImg){
        avatarEl.innerHTML = '<img src="' + t.avatarImg + '" alt="' + t.author + '">';
      } else {
        avatarEl.textContent = t.avatar;
      }
      indexEl.textContent = String(idx+1).padStart(2,"0");
      counterEl.textContent = String(idx+1).padStart(2,"0") + " / " + String(testimonials.length).padStart(2,"0");

      linesEl.innerHTML = "";
      testimonials.forEach(function(_, i){
        var line = document.createElement("div");
        line.className = "edu-line " + (i===idx ? "active" : "inactive");
        line.setAttribute("role", "button");
        line.setAttribute("tabindex", "0");
        line.setAttribute("aria-label", "Ir para depoimento " + (i+1));
        line.onclick = function(){ goToTestimonial(i); };
        line.onkeydown = function(e){ if(e.key==="Enter" || e.key===" ") goToTestimonial(i); };
        linesEl.appendChild(line);
      });

      quoteEl.classList.remove("fade");
      authorWrap.classList.remove("fade");
    }, 250);
  }

  function moveTestimonial(dir){
    if(tTransitioning) return;
    var newIdx = tActive + dir;
    if(newIdx < 0) newIdx = testimonials.length - 1;
    if(newIdx >= testimonials.length) newIdx = 0;
    goToTestimonial(newIdx);
  }

  // Navbar scroll effect
  function initNavbar(){
    var navbar = document.getElementById("navbar");
    if(!navbar) return;
    window.addEventListener("scroll", function(){
      navbar.classList.toggle("nav-scrolled", window.scrollY > 100);
    }, { passive: true });
  }

  // Lenis smooth scroll
  var lenis = null;
  function initLenis(){
    if(typeof Lenis === 'undefined') return;
    document.documentElement.style.scrollBehavior = 'auto';
    lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', function(){
      if(typeof ScrollTrigger !== 'undefined') ScrollTrigger.update();
    });
    if(typeof gsap !== 'undefined'){
      gsap.ticker.add(function(time){ lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(time){ lenis.raf(time); requestAnimationFrame(raf); })(0);
    }
    window.__lenis = lenis;
  }

  // Smooth scroll for anchor links
  function initSmoothScroll(){
    document.querySelectorAll('a[href^="#"]').forEach(function(a){
      a.addEventListener("click", function(e){
        var hash = a.getAttribute("href");
        if(hash.length < 2) return;
        var el = document.querySelector(hash);
        if(el){
          e.preventDefault();
          var navbar = document.getElementById("navbar");
          var offset = navbar ? navbar.offsetHeight : 0;
          if(lenis){
            lenis.scrollTo(el, { offset: -offset });
          } else {
            var top = el.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top: top, behavior: "smooth" });
          }
        }
      });
    });
  }

  // FAQ toggle
  function initFAQ(){
    document.querySelectorAll(".faq-item").forEach(function(item){
      item.addEventListener("click", function(e){
        if(e.target.closest("svg")) return;
        toggleFaq(this);
      });
      item.addEventListener("keydown", function(e){
        if(e.key==="Enter" || e.key===" ") toggleFaq(this);
      });
    });
  }

  function toggleFaq(el){
    document.querySelectorAll(".faq-item").forEach(function(item){
      if(item !== el){
        item.classList.remove("active");
        var ic = item.querySelector("svg");
        if(ic){
          ic.parentElement.style.background = "#fff";
          ic.parentElement.style.color = "var(--text-muted)";
          ic.parentElement.style.border = "1px solid var(--border)";
          ic.innerHTML = '<path d="M12 5v14M5 12h14"/>';
        }
      }
    });
    el.classList.toggle("active");
    var ic = el.querySelector("svg");
    var box = ic.parentElement;
    if(el.classList.contains("active")){
      box.style.background = "var(--primary)";
      box.style.color = "#fff";
      box.style.border = "none";
      ic.innerHTML = '<path d="M18 15l-6-6-6 6"/>';
    } else {
      box.style.background = "#fff";
      box.style.color = "var(--text-muted)";
      box.style.border = "1px solid var(--border)";
      ic.innerHTML = '<path d="M12 5v14M5 12h14"/>';
    }
  }

  // Lazy load images
  function initLazyLoad(){
    if("IntersectionObserver" in window){
      var imgObserver = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            var img = entry.target;
            if(img.dataset.src){
              img.src = img.dataset.src;
              img.removeAttribute("data-src");
            }
            imgObserver.unobserve(img);
          }
        });
      }, { rootMargin: "100px" });
      document.querySelectorAll("img[data-src]").forEach(function(img){
        imgObserver.observe(img);
      });
    }
  }

  // Mobile hamburger menu
  function initMobileNav(){
    var toggle = document.getElementById("nav-toggle");
    var menu = document.getElementById("mobile-menu");
    if(!toggle || !menu) return;
    toggle.addEventListener("click", function(){
      var open = menu.classList.toggle("open");
      toggle.classList.toggle("toggled", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("menu-open", open);
    });
    menu.querySelectorAll("a").forEach(function(a){
      a.addEventListener("click", function(){
        menu.classList.remove("open");
        toggle.classList.remove("toggled");
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("menu-open");
      });
    });
  }

  // Hero headline rotator — alterna entre as duas frases a cada 3.2s
  var heroPhrases = [
    { top: "Seu sorriso", bottom: "em boas mãos." },
    { top: "Atendimento", bottom: "de confiança." }
  ];
  function initHeroRotator(){
    var title = document.getElementById("heroHeadline");
    var topEl = document.getElementById("heroTop");
    var bottomEl = document.getElementById("heroBottom");
    if(!title || !topEl || !bottomEl) return;
    if(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var idx = 0;
    setInterval(function(){
      if(document.hidden) return;
      idx = (idx + 1) % heroPhrases.length;
      title.classList.add("swapping");
      setTimeout(function(){
        topEl.textContent = heroPhrases[idx].top;
        bottomEl.textContent = heroPhrases[idx].bottom;
        title.classList.remove("swapping");
      }, 400);
    }, 3200);
  }

  // Blog cards: tocar mostra a 2ª imagem (mobile)
  function initBlogCards(){
    document.querySelectorAll(".blog-card").forEach(function(card){
      card.addEventListener("click", function(){
        card.classList.toggle("open");
      });
    });
  }

  // GSAP animations
  function initAnimations(){
    if(typeof gsap === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    gsap.from(".hero-media", { scale:1.12, opacity:0, duration:1.1, ease:"power3.out" });
    gsap.from(".hero-reveal", { y:60, opacity:0, duration:1, stagger:0.15, ease:"power3.out", delay:0.85 });

    gsap.utils.toArray(".reveal").forEach(function(el){
      gsap.fromTo(el, { y:50, opacity:0, visibility:"hidden" },
        { y:0, opacity:1, visibility:"visible", duration:0.9, ease:"power3.out",
          scrollTrigger:{ trigger:el, start:"top 85%", toggleActions:"play none none reverse" }
        });
    });

    gsap.utils.toArray(".counter").forEach(function(counter){
      var target = parseInt(counter.getAttribute("data-target"));
      var obj = { val:0 };
      gsap.to(obj, {
        val:target, duration:2, ease:"power2.out",
        scrollTrigger:{ trigger:counter, start:"top 85%", toggleActions:"play none none reverse" },
        onUpdate:function(){ counter.textContent = Math.ceil(obj.val); }
      });
    });

    gsap.utils.toArray(".team-card, .blog-card").forEach(function(card, i){
      gsap.from(card, { y:40, opacity:0, duration:0.7, delay:(i%3)*0.1, scrollTrigger:{ trigger:card, start:"top 90%" } });
    });

    // Parallax hero
    gsap.to(".hero-bg", {
      backgroundPosition:"50% 30%", ease:"none",
      scrollTrigger:{ trigger:".hero-bg", start:"top top", end:"bottom top", scrub:true }
    });

    // Doctor feature — imagem desliza da direita
    gsap.from(".doctor-img img", {
      xPercent:6, opacity:0, duration:1.2, ease:"power3.out",
      scrollTrigger:{ trigger:".doctor-feature", start:"top 75%", toggleActions:"play none none reverse" }
    });

    // Image tilt hover
    document.querySelectorAll("[data-tilt]").forEach(function(el){
      el.addEventListener("mouseenter", function(){
        gsap.to(el, { scale:1.05, duration:0.4, ease:"power2.out" });
      });
      el.addEventListener("mouseleave", function(){
        gsap.to(el, { scale:1, duration:0.4, ease:"power2.out" });
      });
    });
  }

  // Initialize all
  document.addEventListener("DOMContentLoaded", function(){
    initNavbar();
    initLenis();
    initSmoothScroll();
    initFAQ();
    initLazyLoad();
    initAnimations();
    initTestimonials();
    initMobileNav();
    initBlogCards();
    initHeroRotator();
    renderTestimonial(0);

    // Hide service carousel arrows (static grid)
    var prevBtn = document.getElementById("service-prev");
    var nextBtn = document.getElementById("service-next");
    if(prevBtn) prevBtn.style.display = "none";
    if(nextBtn) nextBtn.style.display = "none";
  });
})();