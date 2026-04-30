"""
L'Érudit des Prénoms — Score de Prestige Académique  (V3 · Editorial Scholar)
2 millions de résultats nominatifs · Bac général & technologique · 2012-2020
+ données INSEE naissances 1900-2024 (carte & décennies)

Sources :
  Bac       : Baptiste Coulmont — coulmont.com/bac
  Naissances: INSEE fichier des prénoms
"""

import hashlib
import re
from html import escape as _esc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from src.components import (
    absent_card_html,
    carto_meta_html,
    data_note_html,
    duel_cards_html,
    duel_result_html,
    footer_html,
    gen_card_html,
    gen_rank_html,
    genflop_html,
    hero_html,
    result_card_html,
    section_header_html,
    verdict_card_html,
)
from src.decades import DECADE_VIBES, build_decade_scores, build_peak_years, decade_summary
from src.enrichment import build_enriched_scores
from src.geo import GEOJSON_URL, get_dept_data
from src.insee import load_dpt, load_nat
from src.loader import load_long
from src.normalize import normalize
from src.plotly_theme import (
    COLOR_SEQ,
    COLORSCALE,
    ON_SURF,
    PRIMARY as _P,
    SECONDARY as _S,
    apply_theme,
    gradient_blue,
)
from src.tokens import OUTLINE_FILL, OUTLINE_STRONG
from src.scoring import compute_scores, lookup
from src.styles import PRIMARY, SECONDARY, SURFACE, inject_css

# ── Configuration ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="L'Érudit des Prénoms",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
apply_theme()

# ── Messages humoristiques pour prénoms absents ──────────────────────────────

ABSENT_MSGS = [
    "{p} ? Inconnu au bataillon. Soit ce prénom est rarissime, "
    "soit vos parents ont vraiment voulu vous démarquer.",
    "{p} n'a pas laissé assez de traces sur les bancs du lycée "
    "pour figurer dans nos données. Mystère ou originalité assumée ?",
    "Moins de 40 bacheliers répondant au nom de {p} sur 9 ans. "
    "Votre prénom est soit une œuvre d'art, soit une erreur de registre.",
    "{p} : introuvable. L'algorithme a cherché, il est épuisé. "
    "Essayez une orthographe alternative — ou acceptez d'être une légende.",
]


def _absent_msg(prenom: str) -> str:
    idx = int(hashlib.md5(prenom.encode()).hexdigest(), 16) % len(ABSENT_MSGS)
    return ABSENT_MSGS[idx].format(p=prenom)


# ── Validation d'entrée (sécurité) ───────────────────────────────────────────

_PRENOM_MAX_LEN = 60
_PRENOM_ALLOWED = re.compile(r"[^A-Za-zÀ-ÖØ-öø-ÿ' \-]")


def _sanitize_prenom(raw: str) -> str:
    """Nettoie une saisie utilisateur avant usage :
      - strip + troncature à 60 caractères
      - whitelist : lettres Unicode latines, apostrophe, tiret, espace
    Retourne une chaîne vide si la saisie ne contient aucun caractère valide.
    """
    if not raw:
        return ""
    s = str(raw).strip()[:_PRENOM_MAX_LEN]
    s = _PRENOM_ALLOWED.sub("", s)
    return s


# ── Chargement des données (mis en cache) ────────────────────────────────────

@st.cache_data(show_spinner="Chargement des données bac…")
def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    long = load_long()
    scores_tsv = compute_scores(long)
    # Fusion avec le cache enrichi (scraping Coulmont) — ajoute les prénoms
    # absents du TSV en format cumulé 2012-2020.
    try:
        nat_df = load_nat()
    except Exception:
        nat_df = None
    scores = build_enriched_scores(scores_tsv, nat_df=nat_df)
    return long, scores


@st.cache_data(show_spinner="Calcul de la moyenne nationale…")
def get_nat_avg(long: pd.DataFrame) -> pd.DataFrame:
    return (
        long[long["proptb"].notna()]
        .groupby("year")
        .apply(lambda g: (g["proptb"] * g["N"]).sum() / g["N"].sum(), include_groups=False)
        .reset_index(name="proptb_nat")
    )


@st.cache_data(show_spinner="Chargement des données INSEE nationales…")
def get_decade_data(scores: pd.DataFrame):
    nat_df = load_nat()
    peak_df = build_peak_years(nat_df)
    dec_scores = build_decade_scores(scores, peak_df)
    dec_sum = decade_summary(dec_scores)
    return peak_df, dec_scores, dec_sum


@st.cache_data(show_spinner="Chargement des données INSEE départementales…")
def get_dpt_data():
    dpt_df = load_dpt()
    total_by_dpt = (
        dpt_df.groupby("dpt")["valeur"]
        .sum()
        .reset_index(name="total_dpt")
    )
    return dpt_df, total_by_dpt


@st.cache_resource(show_spinner="Chargement du fond de carte…")
def get_geojson() -> dict:
    r = requests.get(GEOJSON_URL, timeout=30)
    r.raise_for_status()
    return r.json()


# ── Chargement initial ────────────────────────────────────────────────────────

long, scores = get_data()


@st.cache_data(show_spinner=False)
def _get_all_prenoms(prenoms_tuple: tuple) -> list[str]:
    """Liste triée des prénoms — mise en cache pour éviter un sort à chaque rerun."""
    return sorted(prenoms_tuple)


all_prenoms = _get_all_prenoms(tuple(scores["prenom"]))


def _suggest(prefix: str, limit: int = 8) -> list[str]:
    """Suggestions de prénoms partageant les 3 premières lettres."""
    if not prefix:
        return []
    p = prefix[:3].lower()
    return [n for n in all_prenoms if n.lower().startswith(p)][:limit]

# ── Onglets ───────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Anthologie",
    "Le Duel",
    "Tendances",
    "Cartographie",
    "Palmarès",
])

# Streamlit ≥ 1.37 : @st.fragment isole les reruns à l'onglet courant.
# Fallback no-op sur versions antérieures.
_fragment = getattr(st, "fragment", lambda f: f)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ANTHOLOGIE
# ══════════════════════════════════════════════════════════════════════════════

@_fragment
def _render_tab_anthologie() -> None:
    raw = st.text_input(
        "Votre prénom",
        placeholder="ex : Apolline, Sofiane, Gaëtan…",
        key="tab1_input",
        max_chars=_PRENOM_MAX_LEN,
    )
    prenom_input = _sanitize_prenom(raw)

    if not prenom_input:
        n_prenoms = len(scores)
        n_bacheliers = int(scores["effectif_total"].sum())
        st.markdown(
            hero_html(n_prenoms=n_prenoms, n_bacheliers=n_bacheliers),
            unsafe_allow_html=True,
        )
        return

    result = lookup(prenom_input, long, scores)

    if result is None:
        close = _suggest(prenom_input, limit=8)
        st.markdown(
            absent_card_html(prenom_input, _absent_msg(prenom_input), close),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(result_card_html(result), unsafe_allow_html=True)
        st.markdown(verdict_card_html(result), unsafe_allow_html=True)

        # Prénom scrape-only : pas de détail par année → note + breakdown mentions
        if not result.get("history_available", True):
            st.markdown(
                data_note_html(
                    "Données cumulées 2012-2020 — l'évolution par année "
                    "n'est pas publiée pour ce prénom."
                ),
                unsafe_allow_html=True,
            )
            # Graphique breakdown mentions
            mentions = {
                "Oral rattrapage": result.get("pct_oral"),
                "Passable":        result.get("pct_passable"),
                "Assez Bien":      result.get("pct_ab"),
                "Bien":            result.get("pct_bien"),
                "Très Bien":       result.get("pct_tb"),
            }
            mentions = {k: v for k, v in mentions.items() if v is not None}
            if mentions:
                fig = go.Figure(go.Bar(
                    x=list(mentions.keys()),
                    y=list(mentions.values()),
                    marker=dict(color=gradient_blue(len(mentions), 0.25, 0.90)),
                    text=[f"{v:.0f} %" for v in mentions.values()],
                    textposition="outside",
                    hovertemplate="<b>%{x}</b> : %{y:.0f} %<extra></extra>",
                ))
                fig.update_layout(
                    title=f"Répartition des mentions — {_esc(str(result['prenom']))}",
                    yaxis=dict(showgrid=True, tickformat=".0f", ticksuffix=" %"),
                    height=320,
                )
                st.plotly_chart(fig, use_container_width=True)
            return

        # Courbe d'évolution (TSV uniquement)
        hist_df = pd.DataFrame(result["history"])
        if not hist_df.empty and "proptb" in hist_df.columns:
            nat_avg = get_nat_avg(long)

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=nat_avg["year"],
                y=nat_avg["proptb_nat"],
                mode="lines",
                name="Moyenne nationale",
                line=dict(color=OUTLINE_STRONG, width=1.5, dash="dot"),
                fill="tozeroy",
                fillcolor=OUTLINE_FILL,
                hovertemplate="%{y:.1f} %<extra>Moy. nationale</extra>",
            ))

            fig.add_trace(go.Scatter(
                x=hist_df["year"],
                y=hist_df["proptb"],
                mode="lines+markers",
                name=result["prenom"],
                line=dict(color=PRIMARY, width=2.5),
                marker=dict(
                    size=8,
                    color=SECONDARY,
                    line=dict(width=2, color=SURFACE),
                    symbol="diamond",
                ),
                hovertemplate="%{y:.1f} %<extra>" + _esc(str(result["prenom"])) + "</extra>",
            ))

            fig.update_layout(
                title=f"Évolution du % mention Très Bien — {_esc(str(result['prenom']))} {_esc(str(result['sexe_label']))}",
                xaxis=dict(title="", tickformat="d", dtick=1),
                yaxis=dict(
                    title="% Mention TB",
                    rangemode="tozero",
                    showgrid=True,
                    tickformat=".0f", ticksuffix=" %",
                ),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified",
                height=360,
            )
            st.plotly_chart(fig, use_container_width=True)


with tab1:
    _render_tab_anthologie()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LE DUEL
# ══════════════════════════════════════════════════════════════════════════════

@_fragment
def _render_tab_duel() -> None:
    st.markdown(
        section_header_html(
            "Le Duel",
            "Qui méritait vraiment sa mention ?",
            "Comparez deux prénoms sur l'ensemble des données bac 2012-2020.",
        ),
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    raw_a = col_a.text_input("Premier prénom", placeholder="ex : Kévin",
                             key="vs_a", max_chars=_PRENOM_MAX_LEN)
    raw_b = col_b.text_input("Second prénom", placeholder="ex : Adèle",
                             key="vs_b", max_chars=_PRENOM_MAX_LEN)
    prenom_a = _sanitize_prenom(raw_a)
    prenom_b = _sanitize_prenom(raw_b)

    if prenom_a and prenom_b:
        res_a = lookup(prenom_a, long, scores)
        res_b = lookup(prenom_b, long, scores)

        missing = [(n, r) for n, r in [(prenom_a, res_a), (prenom_b, res_b)] if r is None]
        for name, _r in missing:
            close = _suggest(name, limit=6)
            st.markdown(
                absent_card_html(name, _absent_msg(name), close),
                unsafe_allow_html=True,
            )

        if res_a and res_b:
            st.markdown(duel_result_html(res_a, res_b), unsafe_allow_html=True)
            st.markdown(duel_cards_html(res_a, res_b), unsafe_allow_html=True)

            # Graphique comparatif
            hist_a = pd.DataFrame(res_a["history"]).assign(prenom=res_a["prenom"])
            hist_b = pd.DataFrame(res_b["history"]).assign(prenom=res_b["prenom"])
            combined = pd.concat([hist_a, hist_b], ignore_index=True)

            fig = px.line(
                combined,
                x="year",
                y="proptb",
                color="prenom",
                markers=True,
                title="Évolution comparée du % mention Très Bien",
                labels={"year": "Année", "proptb": "% TB", "prenom": "Prénom"},
                color_discrete_sequence=[_P, _S],
            )
            fig.update_traces(
                marker=dict(size=8, symbol="diamond", line=dict(width=2, color=SURFACE)),
                line=dict(width=2.5),
            )
            fig.update_layout(
                hovermode="x unified",
                height=360,
                xaxis=dict(tickformat="d", dtick=1),
                yaxis=dict(showgrid=True, tickformat=".0f", ticksuffix=" %"),
            )
            st.plotly_chart(fig, use_container_width=True)


with tab2:
    _render_tab_duel()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TENDANCES
# ══════════════════════════════════════════════════════════════════════════════

@_fragment
def _render_tab_tendances() -> None:
    st.markdown(
        section_header_html(
            "Tendances",
            "Top des prénoms par millésime",
            "Quels prénoms ont brillé année par année au baccalauréat ?",
        ),
        unsafe_allow_html=True,
    )

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([3, 2, 2])
    year_sel = col_ctrl1.slider("Millésime", min_value=2012, max_value=2020, value=2019)
    n_top    = col_ctrl2.radio("Prénoms affichés", [10, 20], horizontal=True)
    sexe_fil = col_ctrl3.radio("Genre", ["Tous", "♀ Filles", "♂ Garçons"], horizontal=True)

    year_data = long[long["year"] == year_sel].copy()

    if sexe_fil == "♀ Filles":
        year_data = year_data[year_data["sexe"] == 0]
    elif sexe_fil == "♂ Garçons":
        year_data = year_data[year_data["sexe"] == 1]

    year_data = year_data[year_data["N"] >= 80]
    top = year_data.nlargest(n_top, "proptb").copy()

    if top.empty:
        st.info("Pas assez de données pour les filtres sélectionnés.")
    else:
        sorted_top = top.sort_values("proptb").copy()
        sorted_top["label"] = sorted_top["prenom"] + "  (" + sorted_top["N"].astype(str) + ")"
        n = len(sorted_top)

        fig = go.Figure(go.Bar(
            y=sorted_top["label"],
            x=sorted_top["proptb"],
            orientation="h",
            marker=dict(color=gradient_blue(n)),
            text=[f"{v:.1f} %" for v in sorted_top["proptb"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>% Mention TB : %{x:.1f} %<extra></extra>",
        ))
        fig.update_layout(
            title=f"Top {n_top} — % mention Très Bien · {year_sel}",
            xaxis=dict(
                title="", tickformat=".0f", ticksuffix=" %",
                range=[0, sorted_top["proptb"].max() * 1.18],
            ),
            yaxis=dict(title="", categoryorder="total ascending",
                       tickfont=dict(size=11, color=ON_SURF)),
            margin=dict(l=0, r=60, t=48, b=16),
            height=max(420, n_top * 38),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Classement global
    st.markdown("<hr class='es-rule'>", unsafe_allow_html=True)
    st.markdown(
        section_header_html("Palmarès absolu", "Classement général 2012-2020"),
        unsafe_allow_html=True,
    )
    top_global = scores.head(20)[["prenom", "score", "effectif_total", "years_present"]].copy()
    top_global.columns = ["Prénom", "Score TB moy. (%)", "Bacheliers total", "Années de données"]
    top_global["Score TB moy. (%)"] = top_global["Score TB moy. (%)"].round(1)
    st.dataframe(top_global, use_container_width=True, hide_index=True)


with tab3:
    _render_tab_tendances()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CARTOGRAPHIE
# ══════════════════════════════════════════════════════════════════════════════

@_fragment
def _render_tab_carto() -> None:
    st.markdown(
        section_header_html(
            "Cartographie",
            "Géographie d'un prénom",
            "Où en France un prénom est-il le plus populaire ? "
            "L'indice compare chaque département à la moyenne nationale "
            "(1.0 = dans la moyenne · 2.0 = deux fois plus répandu).",
        ),
        unsafe_allow_html=True,
    )

    raw = st.text_input(
        "Prénom à cartographier",
        placeholder="ex : Jordan, Noemie, Baptiste…",
        key="map_input",
        max_chars=_PRENOM_MAX_LEN,
    )
    prenom_map = _sanitize_prenom(raw)

    if prenom_map:
        dpt_df, total_by_dpt = get_dpt_data()
        geojson = get_geojson()
        dept_data = get_dept_data(dpt_df, prenom_map, total_by_dpt)

        if dept_data is None:
            close = _suggest(prenom_map, limit=6)
            st.markdown(
                absent_card_html(
                    prenom_map,
                    f"{prenom_map} : introuvable dans le fichier INSEE. "
                    "Soit ce prénom est rarissime, soit il s'épelle autrement — l'INSEE est pointilleux.",
                    close,
                ),
                unsafe_allow_html=True,
            )
        else:
            total_naissances = int(dept_data["count_prenom"].sum())
            st.markdown(
                carto_meta_html(total_naissances),
                unsafe_allow_html=True,
            )

            fig = px.choropleth(
                dept_data,
                geojson=geojson,
                locations="dpt",
                featureidkey="properties.code",
                color="indice",
                color_continuous_scale=COLORSCALE,
                range_color=[0, dept_data["indice"].quantile(0.95)],
                hover_name="dpt",
                hover_data={
                    "indice": ":.2f",
                    "count_prenom": ":,",
                    "pct": ":.3f",
                    "dpt": False,
                },
                labels={
                    "indice": "Indice",
                    "count_prenom": "Naissances",
                    "pct": "% naissances",
                },
                title=f"Popularité de « {_esc(prenom_map)} » par département",
            )
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                height=550,
                coloraxis_colorbar=dict(title="Indice", tickformat=".1f"),
                margin=dict(l=0, r=0, t=48, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

            top_depts = dept_data.nlargest(10, "indice")[["dpt", "count_prenom", "pct", "indice"]]
            top_depts = top_depts.copy()
            top_depts.columns = ["Département", "Naissances", "% naissances", "Indice"]
            top_depts["% naissances"] = top_depts["% naissances"].round(3)
            st.markdown(
                section_header_html("Analyse", "Top 10 — surreprésentation"),
                unsafe_allow_html=True,
            )
            st.dataframe(top_depts, use_container_width=True, hide_index=True)


with tab4:
    _render_tab_carto()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PALMARÈS
# ══════════════════════════════════════════════════════════════════════════════

@_fragment
def _render_tab_palmares() -> None:
    st.markdown(
        section_header_html(
            "Palmarès",
            "Classement des générations",
            "Les prénoms des années 80 ont-ils un moins bon score que ceux des années 2000 ? "
            "On croise les données bac avec l'année de pic de popularité de chaque prénom (INSEE 1900-2024).",
        ),
        unsafe_allow_html=True,
    )

    peak_df, dec_scores, dec_sum = get_decade_data(scores)

    if dec_scores.empty:
        st.error("Impossible de charger les données INSEE nationales.")
    else:
        # Vue globale : score moyen par décennie
        sorted_dec = dec_sum.sort_values("score_moyen").copy()
        fig_bar = go.Figure(go.Bar(
            y=sorted_dec["decade_label"],
            x=sorted_dec["score_moyen"],
            orientation="h",
            marker=dict(color=gradient_blue(len(sorted_dec))),
            text=[f"{v:.1f} %" for v in sorted_dec["score_moyen"]],
            textposition="outside",
            customdata=sorted_dec[["nb_prenoms", "top_prenom", "bottom_prenom"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>Score moyen : %{x:.1f} %<br>"
                "Prénoms : %{customdata[0]}<br>"
                "🏆 %{customdata[1]}<br>💀 %{customdata[2]}<extra></extra>"
            ),
        ))
        fig_bar.update_layout(
            title="Score moyen de mention TB par génération",
            xaxis=dict(
                title="", tickformat=".1f", ticksuffix=" %",
                range=[0, sorted_dec["score_moyen"].max() * 1.2],
            ),
            yaxis=dict(title="", categoryorder="total ascending",
                       tickfont=dict(size=12, color=ON_SURF)),
            margin=dict(l=0, r=60, t=48, b=16),
            height=380,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Distribution (boxplot)
        decade_colors = {
            label: COLOR_SEQ[i % len(COLOR_SEQ)]
            for i, label in enumerate(sorted(dec_scores["decade_label"].unique()))
        }
        fig_box = px.box(
            dec_scores,
            x="decade_label",
            y="score",
            color="decade_label",
            points="outliers",
            title="Distribution des scores par génération",
            labels={"decade_label": "Génération", "score": "% mention TB", "prenom": "Prénom"},
            hover_data=["prenom"],
            color_discrete_map=decade_colors,
        )
        fig_box.update_traces(
            marker=dict(size=4, opacity=0.6),
            line=dict(width=1.5),
        )
        fig_box.update_layout(
            showlegend=False,
            height=380,
            xaxis=dict(tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, tickformat=".0f", ticksuffix=" %"),
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # Tableau récap
        st.markdown("<hr class='es-rule'>", unsafe_allow_html=True)
        st.markdown(
            section_header_html("Récapitulatif", "Par génération"),
            unsafe_allow_html=True,
        )
        display = dec_sum[[
            "decade_vibe", "decade_label", "score_moyen", "nb_prenoms",
            "top_prenom", "top_score", "bottom_prenom", "bottom_score",
        ]].copy()
        display.columns = [
            "", "Génération", "Score moy. (%)", "Nb prénoms",
            "Meilleur", "Score TB (%)", "Pire", "Score TB (%) ",
        ]
        st.dataframe(display, use_container_width=True, hide_index=True)

        # Cherche ta décennie
        st.markdown("<hr class='es-rule'>", unsafe_allow_html=True)
        st.markdown(
            section_header_html("Exploration", "Trouve ta génération"),
            unsafe_allow_html=True,
        )

        raw_dec = st.text_input(
            "Votre prénom",
            placeholder="ex : Mathieu, Camille, Alexis…",
            key="decade_input",
            max_chars=_PRENOM_MAX_LEN,
        )
        prenom_dec = _sanitize_prenom(raw_dec)

        if prenom_dec:
            result_dec = lookup(prenom_dec, long, scores)
            norm_dec   = normalize(prenom_dec)
            peak_row   = peak_df[peak_df["prenom_norm"] == norm_dec]

            if result_dec is None:
                close = _suggest(prenom_dec, limit=6)
                st.markdown(
                    absent_card_html(prenom_dec, _absent_msg(prenom_dec), close),
                    unsafe_allow_html=True,
                )
            elif peak_row.empty:
                st.markdown(
                    absent_card_html(
                        prenom_dec,
                        f"{prenom_dec} : absent du fichier INSEE naissances. "
                        "Ce prénom échappe à toute classification générationnelle.",
                        [],
                    ),
                    unsafe_allow_html=True,
                )
            else:
                peak_year = int(peak_row.iloc[0]["peak_year"])
                decade    = (peak_year // 10) * 10
                vibe      = DECADE_VIBES.get(decade, "🎓")
                dec_label = f"Années {decade}"

                peers = (
                    dec_scores[dec_scores["decade"] == decade]
                    .sort_values("score", ascending=False)
                    .reset_index(drop=True)
                )
                rank_idx = peers[peers["prenom"].str.lower() == result_dec["prenom"].lower()].index
                rank_num = int(rank_idx[0]) + 1 if len(rank_idx) else None
                rank_str = f"{rank_num} / {len(peers)}" if rank_num else "N/A"

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(gen_card_html(vibe, dec_label, peak_year), unsafe_allow_html=True)
                with col2:
                    st.markdown(
                        gen_rank_html(rank_str, len(peers), result_dec["prenom"]),
                        unsafe_allow_html=True,
                    )

                top3 = peers.head(3)["prenom"].tolist()
                bot3 = peers.tail(3)["prenom"].tolist()
                st.markdown(genflop_html(top3, bot3), unsafe_allow_html=True)


with tab5:
    _render_tab_palmares()


# ── Pied de page ──────────────────────────────────────────────────────────────

st.markdown(footer_html(), unsafe_allow_html=True)
