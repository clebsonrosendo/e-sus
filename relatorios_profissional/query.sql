select
    to_char(tb_atend_prof.dt_inicio, 'DD/MM/YYYY') as "Data",
    tb_prof.nu_cns as "Profissional CNS",
    tb_prof.no_profissional as "Profissional Nome",
    tb_cidadao.no_cidadao as "Paciente Nome",
    tb_cidadao.nu_cns as "Paciente_CNS",
    tb_proced.co_proced as "Procedimentos"
    from tb_atend_prof
left join tb_atend on tb_atend.co_seq_atend = tb_atend_prof.co_atend
left join rl_atend_tipo_servico on rl_atend_tipo_servico.co_atend = tb_atend.co_seq_atend
left join tb_lotacao on tb_lotacao.co_ator_papel = tb_atend_prof.co_lotacao
left join tb_unidade_saude on tb_unidade_saude.co_seq_unidade_saude = tb_lotacao.co_unidade_saude
left join tb_prof on tb_prof.co_seq_prof = tb_lotacao.co_prof
left join rl_atend_proced on tb_atend_prof.co_seq_atend_prof = rl_atend_proced.co_atend_prof
left join tb_cid10 on rl_atend_proced.co_cid10_principal = tb_cid10.co_cid10
left join tb_proced on rl_atend_proced.co_proced = tb_proced.co_seq_proced
left join tb_prontuario on tb_atend.co_prontuario = tb_prontuario.co_seq_prontuario
left join tb_cidadao on tb_prontuario.co_cidadao = tb_cidadao.co_seq_cidadao
    order by
        "Data" asc,
        "Profissional Nome" asc,
        "Paciente Nome" asc