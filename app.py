with tab_menu:
        st.subheader("Ajouter un plat")
        with st.form("add_form", clear_on_submit=True):
            nom = st.text_input("Nom du plat")
            prix = st.number_input("Prix (FCFA)", step=500)
            img = st.text_input("Lien de l'image (URL)")
            if st.form_submit_button("Enregistrer"):
                conn = get_connection()
                conn.cursor().execute('INSERT INTO menu (nom, prix, img) VALUES (?,?,?)', (nom, prix, img))
                conn.commit()
                st.rerun()
        
        st.write("---")
        df_m = pd.read_sql('SELECT * FROM menu', get_connection())
        for _, r in df_m.iterrows():
            c1, c2, c3 = st.columns([1, 3, 1])
            if r['img']: c1.image(r['img'], width=80)
            c2.write(f"**{r['nom']}** - {int(r['prix'])} F")
            if c3.button("🗑️", key=f"m_{r['id']}"):
                get_connection().cursor().execute('DELETE FROM menu WHERE id=?', (r['id'],)).connection.commit()
                st.rerun()

    with tab_histo:
        df_c = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', get_connection())
        st.dataframe(df_c, use_container_width=True)
