"""
Ton Prénom & le Bac — Score de Prestige Académique  (V2)
Basé sur 2M+ résultats nominatifs du bac général et technologique (2012-2020)
+ données INSEE naissances 1900-2024 (carte + décennies)
Source bac : Baptiste Coulmont (coulmont.com/bac)
Source naissance : INSEE fichier des prénoms
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.loader import load_long
from src.scoring import compute_scores, get_verdict, lookup
from src.insee import load_nat, load_dpt
from src.decades import build_peak_years, build_decade_scores, decade_summary
from src.geo import get_dept_data, load_geojson

# ── Configuration ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ton Prénom & le Bac",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Chargement des données (mis en cache) ─────────────────────────────────────

@st.cache_data(show_spinner="Chargement des données...")
def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    long = load_long()
    scores = compute_scores(long)
    return long, scores


long, scores = get_data()
all_prenoms = sorted(scores["prenom"].tolist())

# ── En-tête ───────────────────────────────────────────────────────────────────

st.title("🎓 Ton Prénom & le Bac")
st.caption(
    "2 millions de résultats nominatifs · Bac général & technologique · 2012-2020 · "
    "Source : [Baptiste Coulmont](https://coulmont.com/bac)"
)
st.divider()

# ── Onglets ───────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Mon Prénom",
    "⚔️ Comparateur VS",
    "📊 Top par Année",
    "🗺️ Carte par Département",
    "📅 Classement des Décennies",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Lookup prénom
# ─────────────────────────────────────────────────────────────────────────────

with tab1:
    prenom_input = st.text_input(
        "Saisis ton prénom",
        placeholder="ex : Quitterie, Jérémy, Côme…",
        key="tab1_input",
    )

    if prenom_input:
        result = lookup(prenom_input, long, scores)

        if result is None:
            st.warning(
                f"**{prenom_input}** n'est pas dans le dataset "
                f"(moins de 40 bacheliers recensés sur 2012-2020)."
            )
            # Suggestions de prénoms proches
            close = [p for p in all_prenoms if p.lower().startswith(prenom_input[:3].lower())][:8]
            if close:
                st.caption("Prénoms proches disponibles : " + "  ·  ".join(close))
        else:
            # Métriques clés
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(
                "Score de Prestige",
                f"{result['score']:.1f} %",
                help="% de mention Très Bien moyen, pondéré par l'effectif annuel",
            )
            col2.metric(
                "Percentile",
                f"{result['rank_pct']:.0f} %ile",
                help="Rang parmi tous les prénoms du dataset",
            )
            col3.metric(
                "Bacheliers analysés",
                f"{result['effectif_total']:,}",
            )
            col4.metric(
                "Années de données",
                f"{result['years_present']} / 9",
            )

            # Verdict
            st.info(f"**Le Verdict du Jury :** {result['verdict']}")

            # Courbe d'évolution
            hist_df = pd.DataFrame(result["history"])
            if not hist_df.empty and "proptb" in hist_df.columns:
                nat_avg = long.groupby("year").apply(
                    lambda g: (g["proptb"] * g["N"]).sum() / g["N"].sum()
                ).reset_index(name="proptb_nat")

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=nat_avg["year"], y=nat_avg["proptb_nat"],
                    mode="lines", name="Moyenne nationale",
                    line=dict(color="lightgray", dash="dot"),
                    fill="tozeroy", fillcolor="rgba(200,200,200,0.15)",
                ))
                fig.add_trace(go.Scatter(
                    x=hist_df["year"], y=hist_df["proptb"],
                    mode="lines+markers", name=result["prenom"],
                    line=dict(color="#FF4B4B", width=3),
                    marker=dict(size=8),
                ))
                fig.update_layout(
                    title=f"Évolution du % mention TB — {result['prenom']} {result['sexe_label']}",
                    xaxis_title="Année",
                    yaxis_title="% Mention Très Bien",
                    yaxis=dict(rangemode="tozero"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode="x unified",
                )
                st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Comparateur VS
# ─────────────────────────────────────────────────────────────────────────────

with tab2:
    col_a, _vs, col_b = st.columns([5, 1, 5])
    prenom_a = col_a.text_input("Prénom 1", placeholder="ex : Jérémy", key="vs_a")
    _vs.markdown("<br><br><div style='text-align:center;font-size:1.4rem;font-weight:bold'>VS</div>",
                 unsafe_allow_html=True)
    prenom_b = col_b.text_input("Prénom 2", placeholder="ex : Quitterie", key="vs_b")

    if prenom_a and prenom_b:
        res_a = lookup(prenom_a, long, scores)
        res_b = lookup(prenom_b, long, scores)

        missing = [name for name, res in [(prenom_a, res_a), (prenom_b, res_b)] if res is None]
        for name in missing:
            st.warning(f"**{name}** : absent du dataset (< 40 bacheliers recensés).")

        if res_a and res_b:
            diff = res_a["score"] - res_b["score"]
            if abs(diff) < 0.5:
                st.success("**Match nul.** Vos prénoms sont statistiquement à égalité. "
                           "Décidez à la courte paille.")
            else:
                winner = res_a if diff > 0 else res_b
                loser  = res_b if diff > 0 else res_a
                st.markdown(
                    f"### 🏆 **{winner['prenom']}** domine avec "
                    f"**{winner['score']:.1f} %** de TB vs **{loser['score']:.1f} %**"
                )

            cola, colb = st.columns(2)
            with cola:
                delta = f"{res_a['score'] - res_b['score']:+.1f} pts"
                cola.metric(
                    f"{res_a['prenom']} {res_a['sexe_label']}",
                    f"{res_a['score']:.1f} %",
                    delta,
                )
                st.caption(res_a["verdict"])
            with colb:
                delta = f"{res_b['score'] - res_a['score']:+.1f} pts"
                colb.metric(
                    f"{res_b['prenom']} {res_b['sexe_label']}",
                    f"{res_b['score']:.1f} %",
                    delta,
                )
                st.caption(res_b["verdict"])

            # Graphique comparatif
            hist_a = pd.DataFrame(res_a["history"]).assign(prenom=res_a["prenom"])
            hist_b = pd.DataFrame(res_b["history"]).assign(prenom=res_b["prenom"])
            combined = pd.concat([hist_a, hist_b], ignore_index=True)

            fig = px.line(
                combined, x="year", y="proptb", color="prenom",
                markers=True,
                title="Évolution comparée du % mention Très Bien",
                labels={"year": "Année", "proptb": "% TB", "prenom": "Prénom"},
                color_discrete_sequence=["#FF4B4B", "#1E90FF"],
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Top par Année
# ─────────────────────────────────────────────────────────────────────────────

with tab3:
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([3, 2, 2])
    year_sel = col_ctrl1.slider("Année", min_value=2012, max_value=2020, value=2019)
    n_top    = col_ctrl2.radio("Nombre de prénoms", [10, 20], horizontal=True)
    sexe_fil = col_ctrl3.radio("Genre", ["Tous", "♀ Filles", "♂ Garçons"], horizontal=True)

    year_data = long[long["year"] == year_sel].copy()

    if sexe_fil == "♀ Filles":
        year_data = year_data[year_data["sexe"] == 0]
    elif sexe_fil == "♂ Garçons":
        year_data = year_data[year_data["sexe"] == 1]

    # Filtre N minimum pour éviter les artefacts statistiques
    year_data = year_data[year_data["N"] >= 80]
    top = year_data.nlargest(n_top, "proptb").copy()

    if top.empty:
        st.info("Pas assez de données pour les filtres sélectionnés.")
    else:
        top["label"] = top["prenom"] + "  (" + top["N"].astype(str) + " candidats)"
        fig = px.bar(
            top.sort_values("proptb"),
            x="proptb",
            y="label",
            orientation="h",
            title=f"Top {n_top} prénoms — % mention Très Bien · {year_sel}",
            labels={"proptb": "% Mention Très Bien", "label": ""},
            color="proptb",
            color_continuous_scale="RdYlGn",
            text="proptb",
        )
        fig.update_traces(texttemplate="%{text:.1f} %", textposition="outside")
        fig.update_layout(
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            xaxis_title="% Mention Très Bien",
            height=max(400, n_top * 30),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Classement global (tous prénoms, toutes années confondues)
    st.divider()
    st.subheader("Classement global 2012-2020")
    top_global = scores.head(20)[["prenom", "score", "effectif_total", "years_present"]].copy()
    top_global.columns = ["Prénom", "Score TB moy. (%)", "Bacheliers total", "Années de données"]
    top_global["Score TB moy. (%)"] = top_global["Score TB moy. (%)"].round(1)
    st.dataframe(top_global, use_container_width=True, hide_index=True)


# ── Pied de page ──────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Carte par Département
# ─────────────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown(
        "Où en France un prénom est-il le plus populaire ? "
        "L'**indice** compare la part du prénom dans chaque département "
        "à la moyenne nationale (1.0 = dans la moyenne, 2.0 = deux fois plus répandu)."
    )

    prenom_map = st.text_input(
        "Prénom à cartographier",
        placeholder="ex : Kévin, Inès, Maëlys…",
        key="map_input",
    )

    if prenom_map:
        with st.spinner("Chargement des données INSEE départementales…"):
            dpt_df = load_dpt()
            geojson = load_geojson()

        dept_data = get_dept_data(dpt_df, prenom_map)

        if dept_data is None:
            st.warning(f"**{prenom_map}** : absent du fichier INSEE (prénom trop rare ou orthographe inconnue).")
        else:
            total_naissances = int(dept_data["count_prenom"].sum())
            st.caption(f"Total naissances recensées (1900-2024, France métro) : **{total_naissances:,}**")

            fig = px.choropleth(
                dept_data,
                geojson=geojson,
                locations="dpt",
                featureidkey="properties.code",
                color="indice",
                color_continuous_scale="RdYlGn",
                range_color=[0, dept_data["indice"].quantile(0.95)],
                hover_name="dpt",
                hover_data={"indice": ":.2f", "count_prenom": ":,", "pct": ":.3f", "dpt": False},
                labels={"indice": "Indice", "count_prenom": "Naissances", "pct": "% naissances"},
                title=f"Popularité de « {prenom_map} » par département",
            )
            fig.update_geos(
                fitbounds="locations",
                visible=False,
            )
            fig.update_layout(
                height=550,
                coloraxis_colorbar=dict(title="Indice", tickformat=".1f"),
                margin=dict(l=0, r=0, t=40, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top 10 départements
            top_depts = dept_data.nlargest(10, "indice")[["dpt", "count_prenom", "pct", "indice"]]
            top_depts.columns = ["Département", "Naissances", "% naissances", "Indice"]
            top_depts["% naissances"] = top_depts["% naissances"].round(3)
            st.subheader("Top 10 départements de surreprésentation")
            st.dataframe(top_depts, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — Classement des Décennies
# ─────────────────────────────────────────────────────────────────────────────

with tab5:
    st.markdown(
        "Les prénoms des **années 80** ont-ils vraiment un moins bon score que "
        "ceux des **années 2000** ? On croise les données bac avec l'année de pic "
        "de popularité de chaque prénom (INSEE naissances 1900-2024)."
    )

    with st.spinner("Chargement des données INSEE nationales…"):
        nat_df    = load_nat()
        peak_df   = build_peak_years(nat_df)
        dec_scores = build_decade_scores(scores, peak_df)
        dec_summary = decade_summary(dec_scores)

    if dec_scores.empty:
        st.error("Impossible de charger les données INSEE nationales.")
    else:
        # ── Vue globale : score moyen par décennie ─────────────────────────
        fig_bar = px.bar(
            dec_summary,
            x="decade_label",
            y="score_moyen",
            text="score_moyen",
            color="score_moyen",
            color_continuous_scale="RdYlGn",
            title="Score moyen de mention TB par génération de prénoms",
            labels={"decade_label": "Génération", "score_moyen": "Score moyen (% TB)"},
            hover_data={"nb_prenoms": True, "top_prenom": True, "bottom_prenom": True},
        )
        fig_bar.update_traces(texttemplate="%{text:.1f} %", textposition="outside")
        fig_bar.update_layout(coloraxis_showscale=False, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── Distribution (boxplot) ─────────────────────────────────────────
        fig_box = px.box(
            dec_scores,
            x="decade_label",
            y="score",
            color="decade_label",
            points="outliers",
            title="Distribution des scores par génération",
            labels={"decade_label": "Génération", "score": "% mention TB", "prenom": "Prénom"},
            hover_data=["prenom"],
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

        # ── Tableau récap ──────────────────────────────────────────────────
        st.subheader("Récap par génération")
        display = dec_summary[[
            "decade_vibe", "decade_label", "score_moyen", "nb_prenoms",
            "top_prenom", "top_score", "bottom_prenom", "bottom_score"
        ]].copy()
        display.columns = [
            "", "Génération", "Score moy. (%)", "Nb prénoms",
            "🏆 Meilleur", "Score", "💀 Pire", "Score"
        ]
        st.dataframe(display, use_container_width=True, hide_index=True)

        # ── Cherche ta décennie ────────────────────────────────────────────
        st.divider()
        st.subheader("Trouve ta génération")
        prenom_dec = st.text_input(
            "Ton prénom",
            placeholder="ex : Jérémy, Lucie, Côme…",
            key="decade_input",
        )
        if prenom_dec:
            result_dec = lookup(prenom_dec, long, scores)
            from src.insee import normalize as _norm
            norm_dec = _norm(prenom_dec)
            peak_row = peak_df[peak_df["prenom_norm"] == norm_dec]

            if result_dec is None:
                st.warning(f"**{prenom_dec}** absent du dataset bac.")
            elif peak_row.empty:
                st.warning(f"**{prenom_dec}** absent du fichier INSEE naissances.")
            else:
                peak_year  = int(peak_row.iloc[0]["peak_year"])
                decade     = (peak_year // 10) * 10
                vibe       = {1950:"📻",1960:"✌️",1970:"🕺",1980:"📼",1990:"📟",2000:"💿",2010:"📱"}.get(decade,"🎓")
                dec_label  = f"Années {decade if decade < 2000 else str(decade)}"

                # Rang dans la décennie
                peers = dec_scores[dec_scores["decade"] == decade].sort_values("score", ascending=False).reset_index(drop=True)
                rank_in_dec = peers[peers["prenom"].str.lower() == result_dec["prenom"].lower()].index
                rank_str = f"{int(rank_in_dec[0]) + 1}/{len(peers)}" if len(rank_in_dec) else "N/A"

                col1, col2, col3 = st.columns(3)
                col1.metric(f"{vibe} Génération", dec_label, f"Pic de popularité : {peak_year}")
                col2.metric("Score Bac", f"{result_dec['score']:.1f} %")
                col3.metric("Rang dans sa génération", rank_str)

                st.info(f"**{result_dec['prenom']}** est un prénom des {dec_label}. "
                        f"Dans sa génération, il se classe **{rank_str}**.")

                # Top/bottom de la décennie
                top3   = peers.head(3)["prenom"].tolist()
                bot3   = peers.tail(3)["prenom"].tolist()
                st.caption(f"🏆 Top 3 de ta génération : {', '.join(top3)}")
                st.caption(f"💀 Flop 3 : {', '.join(bot3)}")


# ── Pied de page ──────────────────────────────────────────────────────────────

st.divider()
st.caption(
    "Données bac : Baptiste Coulmont · [coulmont.com/bac](https://coulmont.com/bac) · "
    "Résultats nominatifs publiés par les candidats · Bac général & technologique 2012-2020 · "
    "Données naissances : [INSEE Fichier des prénoms](https://www.insee.fr/fr/statistiques/8595130) · "
    "Seuls les prénoms avec ≥ 40 bacheliers recensés sont inclus."
)
