-- Sito del condominio: tabelle, regole di accesso e archivio dei documenti.
-- Da incollare una volta sola in Supabase > SQL Editor > New query > Run.
-- Ogni alloggio ha un account (creato con strumenti/prepara.py): chi non è
-- collegato a un alloggio non vede niente.

create extension if not exists pgcrypto;

-- ---------- tabelle ----------

create table public.impostazioni (
  id int primary key default 1 check (id = 1),
  nome text not null default 'Condominio',
  email_amministratore text not null default '',
  mese_inizio int not null default 10 check (mese_inizio between 1 and 12),
  modo_scala jsonb not null default '{"1": "rappresentante", "2": "rappresentante"}'
);
insert into public.impostazioni default values;

create table public.alloggi (
  id text primary key,                       -- es. 'S1-07'
  scala int not null,
  interno text not null,
  user_id uuid unique references auth.users on delete set null,
  rappresentante boolean not null default false,
  nome_rappresentante text not null default '',
  gestore boolean not null default false
);

create table public.lettere (
  id uuid primary key default gen_random_uuid(),
  message_id text unique,                    -- per non pubblicare due volte la stessa email
  arrivata date not null default current_date,
  data_lettera date,
  oggetto text not null default '',
  testo_email text not null default '',
  tipo text not null default 'altro' check (tipo in ('convocazione', 'ordinaria', 'riscaldamento', 'verbale', 'altro')),
  gestione text not null,
  allegati jsonb not null default '[]',      -- [{"nome": ..., "percorso": ...}]
  creata_il timestamptz not null default now()
);

create table public.assemblee (
  id uuid primary key default gen_random_uuid(),
  tipo text not null default 'ordinaria' check (tipo in ('ordinaria', 'straordinaria')),
  gestione text not null,
  prima jsonb,                               -- {"data": "2026-11-24", "ora": "07:00", "luogo": "..."}
  seconda jsonb,
  data_riferimento date not null,            -- la data della seconda convocazione, se c'è
  lettera_id uuid references public.lettere on delete set null,
  verbale_id uuid references public.lettere on delete set null
);

create table public.punti (
  id uuid primary key default gen_random_uuid(),
  assemblea_id uuid not null references public.assemblee on delete cascade,
  numero int not null,
  titolo text not null,
  esito text not null default '' check (esito in ('', 'approvato', 'respinto', 'rinviato'))
);

create table public.osservazioni (
  id uuid primary key default gen_random_uuid(),
  alloggio_id text not null references public.alloggi on delete cascade,
  punto_id uuid not null references public.punti on delete cascade,
  testo text not null check (length(testo) between 1 and 4000),
  allegati jsonb not null default '[]',
  stato text not null default 'nuova' check (stato in ('nuova', 'condivisa', 'archiviata')),
  creata_il timestamptz not null default now()
);

create table public.condivisioni (
  id uuid primary key default gen_random_uuid(),
  punto_id uuid not null references public.punti on delete cascade,
  scala int not null,
  osservazione_id uuid references public.osservazioni on delete set null,
  testo text not null,
  allegati jsonb not null default '[]',
  domanda text,                              -- null = nessun sondaggio
  aperto boolean not null default true,
  inoltrata date,
  creata_il timestamptz not null default now()
);

create table public.voti (
  alloggio_id text not null references public.alloggi on delete cascade,
  oggetto_id uuid not null,                  -- una condivisione o un messaggio della bacheca
  scelta text not null check (scelta in ('fav', 'contr', 'ns')),
  primary key (alloggio_id, oggetto_id)
);

create index on public.punti (assemblea_id);
create index on public.osservazioni (punto_id);
create index on public.condivisioni (punto_id);
create index on public.voti (oggetto_id);

-- ---------- funzioni di supporto per le regole ----------

create function public.mio_alloggio() returns text
language sql stable security definer set search_path = public as
$$ select id from alloggi where user_id = auth.uid() $$;

create function public.mia_scala() returns int
language sql stable security definer set search_path = public as
$$ select scala from alloggi where user_id = auth.uid() $$;

create function public.ho_accesso() returns boolean
language sql stable security definer set search_path = public as
$$ select exists (select 1 from alloggi where user_id = auth.uid()) $$;

create function public.sono_gestore() returns boolean
language sql stable security definer set search_path = public as
$$ select coalesce((select gestore from alloggi where user_id = auth.uid()), false) $$;

create function public.sono_rappresentante() returns boolean
language sql stable security definer set search_path = public as
$$ select coalesce((select rappresentante from alloggi where user_id = auth.uid()), false) $$;

create function public.scala_di(alloggio text) returns int
language sql stable security definer set search_path = public as
$$ select scala from alloggi where id = alloggio $$;

create function public.scala_automatica(s int) returns boolean
language sql stable security definer set search_path = public as
$$ select coalesce((select modo_scala ->> s::text from impostazioni) = 'automatica', false) $$;

-- Chi può leggere un'osservazione: chi l'ha scritta, il rappresentante della
-- sua scala, oppure tutti se la scala usa la bacheca automatica.
create function public.posso_vedere_osservazione(alloggio text) returns boolean
language sql stable security definer set search_path = public as
$$ select alloggio = mio_alloggio()
       or (sono_rappresentante() and scala_di(alloggio) = mia_scala())
       or (ho_accesso() and scala_automatica(scala_di(alloggio))) $$;

-- ---------- regole di accesso (RLS) ----------

alter table public.impostazioni enable row level security;
alter table public.alloggi enable row level security;
alter table public.lettere enable row level security;
alter table public.assemblee enable row level security;
alter table public.punti enable row level security;
alter table public.osservazioni enable row level security;
alter table public.condivisioni enable row level security;
alter table public.voti enable row level security;

create policy "leggono gli alloggi" on public.impostazioni for select to authenticated using (ho_accesso());
create policy "modifica il gestore" on public.impostazioni for update to authenticated using (sono_gestore()) with check (sono_gestore());

create policy "leggono gli alloggi" on public.alloggi for select to authenticated using (ho_accesso());

create policy "leggono gli alloggi" on public.lettere for select to authenticated using (ho_accesso());
create policy "corregge il gestore" on public.lettere for update to authenticated using (sono_gestore()) with check (sono_gestore());
create policy "aggiunge il gestore" on public.lettere for insert to authenticated with check (sono_gestore());
create policy "elimina il gestore" on public.lettere for delete to authenticated using (sono_gestore());

create policy "leggono gli alloggi" on public.assemblee for select to authenticated using (ho_accesso());
create policy "gestisce il gestore" on public.assemblee for all to authenticated using (sono_gestore()) with check (sono_gestore());

create policy "leggono gli alloggi" on public.punti for select to authenticated using (ho_accesso());
create policy "gestisce il gestore" on public.punti for all to authenticated using (sono_gestore()) with check (sono_gestore());

create policy "chi può vederle" on public.osservazioni for select to authenticated using (posso_vedere_osservazione(alloggio_id));
create policy "ognuno scrive le sue" on public.osservazioni for insert to authenticated
  with check (alloggio_id = mio_alloggio() and stato = 'nuova');
create policy "ognuno cancella le sue non ancora lette" on public.osservazioni for delete to authenticated
  using (alloggio_id = mio_alloggio() and stato = 'nuova');

create policy "leggono gli alloggi" on public.condivisioni for select to authenticated using (ho_accesso());

create policy "ognuno vede i suoi voti" on public.voti for select to authenticated using (alloggio_id = mio_alloggio());
create policy "ognuno cancella i suoi voti" on public.voti for delete to authenticated using (alloggio_id = mio_alloggio());

-- ---------- azioni (funzioni chiamate dal sito) ----------

-- Voto: uno per alloggio, solo su sondaggi aperti o messaggi della bacheca automatica.
create function public.vota(oggetto uuid, scelta_voto text) returns void
language plpgsql security definer set search_path = public as $$
declare io text := mio_alloggio();
begin
  if io is null then raise exception 'Accesso negato'; end if;
  if not (exists (select 1 from condivisioni where id = oggetto and domanda is not null and aperto)
          or exists (select 1 from osservazioni o where o.id = oggetto and scala_automatica(scala_di(o.alloggio_id)))) then
    raise exception 'Questo sondaggio è chiuso';
  end if;
  if scelta_voto is null then
    delete from voti where alloggio_id = io and oggetto_id = oggetto;
  else
    insert into voti (alloggio_id, oggetto_id, scelta) values (io, oggetto, scelta_voto)
    on conflict (alloggio_id, oggetto_id) do update set scelta = excluded.scelta;
  end if;
end $$;

-- Totali dei voti, senza dire chi ha votato cosa.
create function public.conteggi() returns table (oggetto_id uuid, fav int, contr int, ns int)
language sql stable security definer set search_path = public as $$
  select oggetto_id,
         count(*) filter (where scelta = 'fav')::int,
         count(*) filter (where scelta = 'contr')::int,
         count(*) filter (where scelta = 'ns')::int
  from voti where ho_accesso() group by oggetto_id $$;

-- Il rappresentante condivide un'osservazione della sua scala, senza nome e interno.
create function public.condividi(oss uuid, testo_condiviso text, domanda_sondaggio text) returns uuid
language plpgsql security definer set search_path = public as $$
declare o osservazioni; nuovo uuid;
begin
  select * into o from osservazioni where id = oss;
  if o.id is null or not sono_rappresentante() or scala_di(o.alloggio_id) <> mia_scala() then
    raise exception 'Accesso negato';
  end if;
  insert into condivisioni (punto_id, scala, osservazione_id, testo, allegati, domanda)
  values (o.punto_id, mia_scala(), o.id, coalesce(nullif(trim(testo_condiviso), ''), o.testo), o.allegati,
          nullif(trim(coalesce(domanda_sondaggio, '')), ''))
  returning id into nuovo;
  update osservazioni set stato = 'condivisa' where id = oss;
  return nuovo;
end $$;

create function public.cambia_stato_osservazione(oss uuid, nuovo_stato text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if nuovo_stato not in ('nuova', 'archiviata') or not sono_rappresentante()
     or (select scala_di(alloggio_id) from osservazioni where id = oss) is distinct from mia_scala() then
    raise exception 'Accesso negato';
  end if;
  update osservazioni set stato = nuovo_stato where id = oss and stato <> 'condivisa';
end $$;

create function public.aggiorna_condivisione(cond uuid, chiudi boolean, segna_inoltrata boolean) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not sono_rappresentante() or (select scala from condivisioni where id = cond) is distinct from mia_scala() then
    raise exception 'Accesso negato';
  end if;
  update condivisioni set aperto = case when chiudi then false else aperto end,
                          inoltrata = case when segna_inoltrata then current_date else inoltrata end
  where id = cond;
end $$;

-- Il gestore sceglie il rappresentante di una scala (alloggio null = nessuno).
create function public.imposta_rappresentante(s int, alloggio text, nome text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if not sono_gestore() then raise exception 'Accesso negato'; end if;
  update alloggi set rappresentante = false, nome_rappresentante = '' where scala = s;
  if alloggio is not null then
    update alloggi set rappresentante = true, nome_rappresentante = coalesce(trim(nome), '')
    where id = alloggio and scala = s;
  end if;
end $$;

-- Per la pagina di accesso, prima del login: nome del condominio ed elenco degli alloggi.
create function public.pagina_accesso() returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'nome', (select nome from impostazioni),
    'alloggi', coalesce((select jsonb_agg(jsonb_build_object('id', id, 'scala', scala, 'interno', interno)
                          order by scala, length(interno), interno) from alloggi), '[]'::jsonb)) $$;

revoke execute on all functions in schema public from public, anon;
grant execute on all functions in schema public to authenticated;
grant execute on function public.pagina_accesso() to anon;

-- ---------- archivio dei documenti (PDF e foto) ----------

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('documenti', 'documenti', false, 20971520,
        array['application/pdf', 'image/jpeg', 'image/png', 'image/webp']);

-- lettere/...                      i PDF dell'amministratore (li carica il lettore)
-- osservazioni/<alloggio>/...      gli allegati delle osservazioni
create function public.posso_vedere_file(percorso text) returns boolean
language sql stable security definer set search_path = public as $$
  select ho_accesso() and (
    split_part(percorso, '/', 1) = 'lettere'
    or (split_part(percorso, '/', 1) = 'osservazioni' and (
          posso_vedere_osservazione(split_part(percorso, '/', 2))
          or exists (select 1 from condivisioni c, jsonb_array_elements(c.allegati) a where a ->> 'percorso' = percorso)))) $$;
grant execute on function public.posso_vedere_file(text) to authenticated;

create policy "condomini leggono i documenti" on storage.objects for select to authenticated
  using (bucket_id = 'documenti' and public.posso_vedere_file(name));
create policy "condomini caricano i propri allegati" on storage.objects for insert to authenticated
  with check (bucket_id = 'documenti' and split_part(name, '/', 1) = 'osservazioni'
              and split_part(name, '/', 2) = public.mio_alloggio());
create policy "il gestore carica le lettere" on storage.objects for insert to authenticated
  with check (bucket_id = 'documenti' and split_part(name, '/', 1) = 'lettere' and public.sono_gestore());
