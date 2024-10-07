const {
  SvelteComponent: x,
  append: H,
  attr: r,
  bubble: $,
  check_outros: ee,
  create_slot: J,
  detach: q,
  element: A,
  empty: le,
  get_all_dirty_from_scope: K,
  get_slot_changes: M,
  group_outros: ie,
  init: ne,
  insert: S,
  listen: te,
  safe_not_equal: oe,
  set_style: h,
  space: O,
  src_url_equal: j,
  toggle_class: k,
  transition_in: R,
  transition_out: T,
  update_slot_base: Q
} = window.__gradio__svelte__internal;
function fe(i) {
  let e, l, s, o, a, d, u = (
    /*icon*/
    i[7] && D(i)
  );
  const t = (
    /*#slots*/
    i[12].default
  ), f = J(
    t,
    i,
    /*$$scope*/
    i[11],
    null
  );
  return {
    c() {
      e = A("button"), u && u.c(), l = O(), f && f.c(), r(e, "class", s = /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-8huxfn"), r(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), e.disabled = /*disabled*/
      i[8], k(e, "hidden", !/*visible*/
      i[2]), h(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), h(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), h(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(n, c) {
      S(n, e, c), u && u.m(e, null), H(e, l), f && f.m(e, null), o = !0, a || (d = te(
        e,
        "click",
        /*click_handler*/
        i[13]
      ), a = !0);
    },
    p(n, c) {
      /*icon*/
      n[7] ? u ? u.p(n, c) : (u = D(n), u.c(), u.m(e, l)) : u && (u.d(1), u = null), f && f.p && (!o || c & /*$$scope*/
      2048) && Q(
        f,
        t,
        n,
        /*$$scope*/
        n[11],
        o ? M(
          t,
          /*$$scope*/
          n[11],
          c,
          null
        ) : K(
          /*$$scope*/
          n[11]
        ),
        null
      ), (!o || c & /*size, variant, elem_classes*/
      26 && s !== (s = /*size*/
      n[4] + " " + /*variant*/
      n[3] + " " + /*elem_classes*/
      n[1].join(" ") + " svelte-8huxfn")) && r(e, "class", s), (!o || c & /*elem_id*/
      1) && r(
        e,
        "id",
        /*elem_id*/
        n[0]
      ), (!o || c & /*disabled*/
      256) && (e.disabled = /*disabled*/
      n[8]), (!o || c & /*size, variant, elem_classes, visible*/
      30) && k(e, "hidden", !/*visible*/
      n[2]), c & /*scale*/
      512 && h(
        e,
        "flex-grow",
        /*scale*/
        n[9]
      ), c & /*scale*/
      512 && h(
        e,
        "width",
        /*scale*/
        n[9] === 0 ? "fit-content" : null
      ), c & /*min_width*/
      1024 && h(e, "min-width", typeof /*min_width*/
      n[10] == "number" ? `calc(min(${/*min_width*/
      n[10]}px, 100%))` : null);
    },
    i(n) {
      o || (R(f, n), o = !0);
    },
    o(n) {
      T(f, n), o = !1;
    },
    d(n) {
      n && q(e), u && u.d(), f && f.d(n), a = !1, d();
    }
  };
}
function ue(i) {
  let e, l, s, o, a = (
    /*icon*/
    i[7] && F(i)
  );
  const d = (
    /*#slots*/
    i[12].default
  ), u = J(
    d,
    i,
    /*$$scope*/
    i[11],
    null
  );
  return {
    c() {
      e = A("a"), a && a.c(), l = O(), u && u.c(), r(
        e,
        "href",
        /*link*/
        i[6]
      ), r(e, "rel", "noopener noreferrer"), r(
        e,
        "aria-disabled",
        /*disabled*/
        i[8]
      ), r(e, "class", s = /*size*/
      i[4] + " " + /*variant*/
      i[3] + " " + /*elem_classes*/
      i[1].join(" ") + " svelte-8huxfn"), r(
        e,
        "id",
        /*elem_id*/
        i[0]
      ), k(e, "hidden", !/*visible*/
      i[2]), k(
        e,
        "disabled",
        /*disabled*/
        i[8]
      ), h(
        e,
        "flex-grow",
        /*scale*/
        i[9]
      ), h(
        e,
        "pointer-events",
        /*disabled*/
        i[8] ? "none" : null
      ), h(
        e,
        "width",
        /*scale*/
        i[9] === 0 ? "fit-content" : null
      ), h(e, "min-width", typeof /*min_width*/
      i[10] == "number" ? `calc(min(${/*min_width*/
      i[10]}px, 100%))` : null);
    },
    m(t, f) {
      S(t, e, f), a && a.m(e, null), H(e, l), u && u.m(e, null), o = !0;
    },
    p(t, f) {
      /*icon*/
      t[7] ? a ? a.p(t, f) : (a = F(t), a.c(), a.m(e, l)) : a && (a.d(1), a = null), u && u.p && (!o || f & /*$$scope*/
      2048) && Q(
        u,
        d,
        t,
        /*$$scope*/
        t[11],
        o ? M(
          d,
          /*$$scope*/
          t[11],
          f,
          null
        ) : K(
          /*$$scope*/
          t[11]
        ),
        null
      ), (!o || f & /*link*/
      64) && r(
        e,
        "href",
        /*link*/
        t[6]
      ), (!o || f & /*disabled*/
      256) && r(
        e,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), (!o || f & /*size, variant, elem_classes*/
      26 && s !== (s = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn")) && r(e, "class", s), (!o || f & /*elem_id*/
      1) && r(
        e,
        "id",
        /*elem_id*/
        t[0]
      ), (!o || f & /*size, variant, elem_classes, visible*/
      30) && k(e, "hidden", !/*visible*/
      t[2]), (!o || f & /*size, variant, elem_classes, disabled*/
      282) && k(
        e,
        "disabled",
        /*disabled*/
        t[8]
      ), f & /*scale*/
      512 && h(
        e,
        "flex-grow",
        /*scale*/
        t[9]
      ), f & /*disabled*/
      256 && h(
        e,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), f & /*scale*/
      512 && h(
        e,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), f & /*min_width*/
      1024 && h(e, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    i(t) {
      o || (R(u, t), o = !0);
    },
    o(t) {
      T(u, t), o = !1;
    },
    d(t) {
      t && q(e), a && a.d(), u && u.d(t);
    }
  };
}
function D(i) {
  let e, l, s;
  return {
    c() {
      e = A("img"), r(e, "class", "button-icon svelte-8huxfn"), j(e.src, l = /*icon*/
      i[7].url) || r(e, "src", l), r(e, "alt", s = `${/*value*/
      i[5]} icon`);
    },
    m(o, a) {
      S(o, e, a);
    },
    p(o, a) {
      a & /*icon*/
      128 && !j(e.src, l = /*icon*/
      o[7].url) && r(e, "src", l), a & /*value*/
      32 && s !== (s = `${/*value*/
      o[5]} icon`) && r(e, "alt", s);
    },
    d(o) {
      o && q(e);
    }
  };
}
function F(i) {
  let e, l, s;
  return {
    c() {
      e = A("img"), r(e, "class", "button-icon svelte-8huxfn"), j(e.src, l = /*icon*/
      i[7].url) || r(e, "src", l), r(e, "alt", s = `${/*value*/
      i[5]} icon`);
    },
    m(o, a) {
      S(o, e, a);
    },
    p(o, a) {
      a & /*icon*/
      128 && !j(e.src, l = /*icon*/
      o[7].url) && r(e, "src", l), a & /*value*/
      32 && s !== (s = `${/*value*/
      o[5]} icon`) && r(e, "alt", s);
    },
    d(o) {
      o && q(e);
    }
  };
}
function se(i) {
  let e, l, s, o;
  const a = [ue, fe], d = [];
  function u(t, f) {
    return (
      /*link*/
      t[6] && /*link*/
      t[6].length > 0 ? 0 : 1
    );
  }
  return e = u(i), l = d[e] = a[e](i), {
    c() {
      l.c(), s = le();
    },
    m(t, f) {
      d[e].m(t, f), S(t, s, f), o = !0;
    },
    p(t, [f]) {
      let n = e;
      e = u(t), e === n ? d[e].p(t, f) : (ie(), T(d[n], 1, 1, () => {
        d[n] = null;
      }), ee(), l = d[e], l ? l.p(t, f) : (l = d[e] = a[e](t), l.c()), R(l, 1), l.m(s.parentNode, s));
    },
    i(t) {
      o || (R(l), o = !0);
    },
    o(t) {
      T(l), o = !1;
    },
    d(t) {
      t && q(s), d[e].d(t);
    }
  };
}
function ae(i, e, l) {
  let { $$slots: s = {}, $$scope: o } = e, { elem_id: a = "" } = e, { elem_classes: d = [] } = e, { visible: u = !0 } = e, { variant: t = "secondary" } = e, { size: f = "lg" } = e, { value: n = null } = e, { link: c = null } = e, { icon: b = null } = e, { disabled: w = !1 } = e, { scale: z = null } = e, { min_width: E = void 0 } = e;
  function B(m) {
    $.call(this, i, m);
  }
  return i.$$set = (m) => {
    "elem_id" in m && l(0, a = m.elem_id), "elem_classes" in m && l(1, d = m.elem_classes), "visible" in m && l(2, u = m.visible), "variant" in m && l(3, t = m.variant), "size" in m && l(4, f = m.size), "value" in m && l(5, n = m.value), "link" in m && l(6, c = m.link), "icon" in m && l(7, b = m.icon), "disabled" in m && l(8, w = m.disabled), "scale" in m && l(9, z = m.scale), "min_width" in m && l(10, E = m.min_width), "$$scope" in m && l(11, o = m.$$scope);
  }, [
    a,
    d,
    u,
    t,
    f,
    n,
    c,
    b,
    w,
    z,
    E,
    o,
    s,
    B
  ];
}
class _e extends x {
  constructor(e) {
    super(), ne(this, e, ae, se, oe, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: ce,
  append: P,
  attr: L,
  create_component: me,
  destroy_component: de,
  detach: U,
  element: G,
  init: re,
  insert: V,
  listen: be,
  mount_component: he,
  safe_not_equal: ge,
  set_data: W,
  space: ve,
  text: X,
  transition_in: ke,
  transition_out: we
} = window.__gradio__svelte__internal;
function ze(i) {
  let e = (
    /*value*/
    (i[3] ? (
      /*gradio*/
      i[14].i18n(
        /*value*/
        i[3]
      )
    ) : "") + ""
  ), l;
  return {
    c() {
      l = X(e);
    },
    m(s, o) {
      V(s, l, o);
    },
    p(s, o) {
      o & /*value, gradio*/
      16392 && e !== (e = /*value*/
      (s[3] ? (
        /*gradio*/
        s[14].i18n(
          /*value*/
          s[3]
        )
      ) : "") + "") && W(l, e);
    },
    d(s) {
      s && U(l);
    }
  };
}
function Ee(i) {
  let e, l, s, o, a, d, u, t, f;
  return l = new _e({
    props: {
      value: (
        /*value*/
        i[3]
      ),
      variant: (
        /*variant*/
        i[4]
      ),
      elem_id: (
        /*elem_id*/
        i[0]
      ),
      elem_classes: (
        /*elem_classes*/
        i[1]
      ),
      size: (
        /*size*/
        i[6]
      ),
      scale: (
        /*scale*/
        i[7]
      ),
      link: (
        /*link*/
        i[9]
      ),
      icon: (
        /*icon*/
        i[8]
      ),
      min_width: (
        /*min_width*/
        i[10]
      ),
      visible: (
        /*visible*/
        i[2]
      ),
      disabled: !/*interactive*/
      i[5],
      $$slots: { default: [ze] },
      $$scope: { ctx: i }
    }
  }), l.$on(
    "click",
    /*click_handler*/
    i[18]
  ), {
    c() {
      e = G("div"), me(l.$$.fragment), s = ve(), o = G("span"), a = X(
        /*tooltip*/
        i[11]
      ), L(o, "class", "tooltip-text svelte-of72zt"), L(e, "class", "tooltip-container svelte-of72zt"), L(e, "style", d = `--tooltip-color: ${/*tooltip_color*/
      i[12]}; --tooltip-background-color: ${/*tooltip_background_color*/
      i[13]}`);
    },
    m(n, c) {
      V(n, e, c), he(l, e, null), P(e, s), P(e, o), P(o, a), u = !0, t || (f = be(
        e,
        "mouseenter",
        /*calculateTooltipPosition*/
        i[15]
      ), t = !0);
    },
    p(n, [c]) {
      const b = {};
      c & /*value*/
      8 && (b.value = /*value*/
      n[3]), c & /*variant*/
      16 && (b.variant = /*variant*/
      n[4]), c & /*elem_id*/
      1 && (b.elem_id = /*elem_id*/
      n[0]), c & /*elem_classes*/
      2 && (b.elem_classes = /*elem_classes*/
      n[1]), c & /*size*/
      64 && (b.size = /*size*/
      n[6]), c & /*scale*/
      128 && (b.scale = /*scale*/
      n[7]), c & /*link*/
      512 && (b.link = /*link*/
      n[9]), c & /*icon*/
      256 && (b.icon = /*icon*/
      n[8]), c & /*min_width*/
      1024 && (b.min_width = /*min_width*/
      n[10]), c & /*visible*/
      4 && (b.visible = /*visible*/
      n[2]), c & /*interactive*/
      32 && (b.disabled = !/*interactive*/
      n[5]), c & /*$$scope, value, gradio*/
      1064968 && (b.$$scope = { dirty: c, ctx: n }), l.$set(b), (!u || c & /*tooltip*/
      2048) && W(
        a,
        /*tooltip*/
        n[11]
      ), (!u || c & /*tooltip_color, tooltip_background_color*/
      12288 && d !== (d = `--tooltip-color: ${/*tooltip_color*/
      n[12]}; --tooltip-background-color: ${/*tooltip_background_color*/
      n[13]}`)) && L(e, "style", d);
    },
    i(n) {
      u || (ke(l.$$.fragment, n), u = !0);
    },
    o(n) {
      we(l.$$.fragment, n), u = !1;
    },
    d(n) {
      n && U(e), de(l), t = !1, f();
    }
  };
}
function qe(i, e, l) {
  let { elem_id: s = "" } = e, { elem_classes: o = [] } = e, { visible: a = !0 } = e, { value: d } = e, { variant: u = "secondary" } = e, { interactive: t } = e, { size: f = "lg" } = e, { scale: n = null } = e, { icon: c = null } = e, { link: b = null } = e, { min_width: w = void 0 } = e, { tooltip: z } = e, { tooltip_color: E = "white" } = e, { tooltip_background_color: B = "black" } = e, { x: m = null } = e, { y: C = null } = e, { gradio: I } = e;
  function N(_) {
    const v = _.currentTarget, g = v.querySelector(".tooltip-text");
    if (v && g)
      if (m !== null && C !== null)
        g.style.left = `${m}px`, g.style.top = `${C}px`;
      else {
        const y = v.getBoundingClientRect();
        g.getBoundingClientRect(), g.style.left = "50%";
        const p = 5;
        g.style.bottom = `${y.height + p}px`, g.style.top = "auto";
      }
  }
  window.addEventListener("resize", () => {
    document.querySelectorAll(".tooltip-text").forEach((v) => {
      const g = v.parentElement;
      N({ currentTarget: g });
    });
  });
  function Y() {
    document.querySelectorAll(".tooltip-container button").forEach((v) => {
      v.addEventListener("mouseenter", N), v.addEventListener("mouseleave", () => {
        const g = v.querySelector(".tooltip-text");
        g.style.visibility = "hidden";
      });
    });
  }
  window.addEventListener("load", Y);
  const Z = () => I.dispatch("click");
  return i.$$set = (_) => {
    "elem_id" in _ && l(0, s = _.elem_id), "elem_classes" in _ && l(1, o = _.elem_classes), "visible" in _ && l(2, a = _.visible), "value" in _ && l(3, d = _.value), "variant" in _ && l(4, u = _.variant), "interactive" in _ && l(5, t = _.interactive), "size" in _ && l(6, f = _.size), "scale" in _ && l(7, n = _.scale), "icon" in _ && l(8, c = _.icon), "link" in _ && l(9, b = _.link), "min_width" in _ && l(10, w = _.min_width), "tooltip" in _ && l(11, z = _.tooltip), "tooltip_color" in _ && l(12, E = _.tooltip_color), "tooltip_background_color" in _ && l(13, B = _.tooltip_background_color), "x" in _ && l(16, m = _.x), "y" in _ && l(17, C = _.y), "gradio" in _ && l(14, I = _.gradio);
  }, [
    s,
    o,
    a,
    d,
    u,
    t,
    f,
    n,
    c,
    b,
    w,
    z,
    E,
    B,
    I,
    N,
    m,
    C,
    Z
  ];
}
class Se extends ce {
  constructor(e) {
    super(), re(this, e, qe, Ee, ge, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      value: 3,
      variant: 4,
      interactive: 5,
      size: 6,
      scale: 7,
      icon: 8,
      link: 9,
      min_width: 10,
      tooltip: 11,
      tooltip_color: 12,
      tooltip_background_color: 13,
      x: 16,
      y: 17,
      gradio: 14
    });
  }
}
export {
  _e as BaseButton,
  Se as default
};
