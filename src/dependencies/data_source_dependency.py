from src.data.data_source import DataSource
from src.data.supabase_data_source import SupabaseDataSource

def get_supabase_data_source() -> DataSource:
    return SupabaseDataSource()