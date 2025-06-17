from django.db.models import Lookup, Field


@Field.register_lookup
class InContainsLookup(Lookup):
    lookup_name = "incontains"
    # Vamos preparar a própria rhs, sem delegar ao comportamento padrão
    prepare_rhs = False

    def get_prep_lookup(self):
        """
        Prepara self.rhs para o SQL:
        - Se for lista/tupla, junta em uma string "termo1,termo2"
        - Caso contrário, usa o valor como veio
        """
        rhs = self.rhs
        if isinstance(rhs, (list, tuple)):
            termos = [str(v).replace(",", " ").strip() for v in rhs]
            return ",".join(termos)
        return super().get_prep_lookup()

    # :contentReference[oaicite:0]{index=0}

    def as_sql(self, compiler, connection):
        # compila o lado esquerdo (campo)
        lhs_sql, lhs_params = self.process_lhs(compiler, connection)

        # pega a string preparada, ex: "couro marrom,fecho metálico"
        lookup_value = self.get_prep_lookup()
        # separa de volta em termos
        termos = [t for t in lookup_value.split(",") if t.strip()]
        # envolve cada termo em %…% para o ILIKE
        patterns = [f"%{t}%" for t in termos]

        # gera placeholders (%s, %s, …) de acordo com o número de termos
        placeholders = ",".join("%s" for _ in patterns)

        sql = f"UNACCENT({lhs_sql}) ILIKE ANY (ARRAY[{placeholders}])"
        return sql, patterns

    def get_db_prep_lookup(self, value, connection):
        """
        Este método é chamado depois de get_prep_lookup() e recebe:
         - value: o que get_prep_lookup() retornou
         - connection: a conexão atual
        Aqui podemos converter o `value` em algo que o banco entenda.
        """
        # Se quisermos, podemos usar connection.ops para adaptar valor,
        # mas neste caso vamos só repassar como um único parâmetro.
        return "%s", [value]
    # :contentReference[oaicite:1]{index=1}
