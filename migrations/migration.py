import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def create_normalized_tables():
    if not DATABASE_URL:
        print("Variável DATABASE_URL não encontrada no .env")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        create_macro_tema_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS macro_tema (
                id SERIAL PRIMARY KEY,
                macro_tema TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute(create_macro_tema_query)
        print("Tabela 'macro_tema' criada ou já existente.")

        create_lbl_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS lbl (
                id SERIAL PRIMARY KEY,
                lbl INTEGER NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                descricao TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute(create_lbl_query)
        print("Tabela 'lbl' criada ou já existente.")

        create_area_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS area (
                id SERIAL PRIMARY KEY,
                area TEXT NOT NULL,
                macro_tema_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (macro_tema_id) REFERENCES macro_tema(id) ON DELETE CASCADE
            );
        """)
        cur.execute(create_area_query)
        print("Tabela 'area' criada ou já existente.")

        create_subarea_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS subarea (
                id SERIAL PRIMARY KEY,
                subarea TEXT NOT NULL,
                area_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (area_id) REFERENCES area(id) ON DELETE CASCADE
            );
        """)
        cur.execute(create_subarea_query)
        print("Tabela 'subarea' criada ou já existente.")

        create_disciplina_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS disciplina (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                subarea_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subarea_id) REFERENCES subarea(id) ON DELETE CASCADE
            );
        """)
        cur.execute(create_disciplina_query)
        print("Tabela 'disciplina' criada ou já existente.")

        create_assunto_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS assunto (
                id SERIAL PRIMARY KEY,
                assunto TEXT NOT NULL,
                disciplina_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (disciplina_id) REFERENCES disciplina(id) ON DELETE CASCADE
            );
        """)
        cur.execute(create_assunto_query)
        print("Tabela 'assunto' criada ou já existente. (FK para 'disciplina')")

        create_assunto_lbl_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS assunto_lbl (
                assunto_id INTEGER NOT NULL,
                lbl_id INTEGER NOT NULL,
                PRIMARY KEY (assunto_id, lbl_id),
                FOREIGN KEY (assunto_id) REFERENCES assunto(id) ON DELETE CASCADE,
                FOREIGN KEY (lbl_id) REFERENCES lbl(id) ON DELETE CASCADE
            );
        """)
        cur.execute(create_assunto_lbl_query)
        print("Tabela 'assunto_lbl' criada ou já existente.")

        create_indexes_queries = [
            "CREATE INDEX IF NOT EXISTS idx_area_macro_tema ON area(macro_tema_id);",
            "CREATE INDEX IF NOT EXISTS idx_subarea_area ON subarea(area_id);",
            "CREATE INDEX IF NOT EXISTS idx_disciplina_subarea ON disciplina(subarea_id);",
            "CREATE INDEX IF NOT EXISTS idx_assunto_disciplina ON assunto(disciplina_id);",
            "CREATE INDEX IF NOT EXISTS idx_assunto_lbl_assunto ON assunto_lbl(assunto_id);",
            "CREATE INDEX IF NOT EXISTS idx_assunto_lbl_lbl ON assunto_lbl(lbl_id);"
        ]
        
        for index_query in create_indexes_queries:
            cur.execute(index_query)
        
        print("Índices criados ou já existentes.")

        conn.commit()
        print("\n✅ Todas as tabelas foram criadas com sucesso!")
        print("\nEstrutura criada:")
        print("- macro_tema (id, macro_tema, timestamp)")
        print("- lbl (id, lbl, nome, descricao, timestamp) - VAZIA para cadastro manual")
        print("- area (id, area, macro_tema_id, timestamp)")
        print("- subarea (id, subarea, area_id, timestamp)")
        print("- disciplina (id, nome, subarea_id, timestamp)")
        print("- assunto (id, assunto, disciplina_id, timestamp)")
        print("- assunto_lbl (assunto_id, lbl_id)")

        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

def drop_old_table():
    """Remove a tabela antiga 'temas' se existir"""
    if not DATABASE_URL:
        print("Variável DATABASE_URL não encontrada no .env")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'temas'
            );
        """)
        
        table_exists = cur.fetchone()[0]
        
        if table_exists:
            response = input("A tabela antiga 'temas' foi encontrada. Deseja removê-la? (s/n): ")
            if response.lower() in ['s', 'sim', 'y', 'yes']:
                cur.execute("DROP TABLE temas")
                conn.commit()
                print("Tabela antiga 'temas' removida.")
            else:
                print("Tabela antiga 'temas' mantida.")
        else:
            print("Tabela antiga 'temas' não encontrada.")

        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Erro ao verificar/remover tabela antiga: {e}")

if __name__ == "__main__":
    print("🔄 Iniciando migração para estrutura normalizada...")
    print("=" * 50)
    
    create_normalized_tables()
    
    drop_old_table()
    
    print("=" * 50)
    print("✅ Migração concluída!")
    print("\n📝 Próximos passos:")
    print("1. Cadastre os LBLs (incluindo o campo 'descricao') na tabela 'lbl'")
    print("2. Cadastre os macro temas na tabela 'macro_tema'")
    print("3. Cadastre as áreas em 'area' → subáreas em 'subarea' → disciplinas em 'disciplina'")
    print("4. Cadastre assuntos em 'assunto' (relacionados a uma disciplina)")
    print("5. Relacione assuntos com LBLs na tabela 'assunto_lbl'")
