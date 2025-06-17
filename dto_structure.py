NOTA_FISCAL_DTO = """       
public class NotaFiscal
{
    public string Numero { get; set; }
    public DateTime DataEmissao { get; set; }
    public DateTime? PeriodoNotaFiscalInicio { get; set; }
    public DateTime? PeriodoNotaFiscalFim { get; set; }
    public string Tipo { get; set; }
    public string Modelo { get; set; }
    public string IdentificadorPessoaCliente { get; set; }
    public string IdentificadorPessoaFornecedor { get; set; }
    public string NumeroDocumentoFiscal { get; set; }
    public string CFOP { get; set; }
    public string Serie { get; set; }
    public decimal ValorTotal { get; set; }
    public string ObservacaoNotaFiscal { get; set; }
    public string ReservadoFisco { get; set; }
    public string ChaveAcessoNotaFiscal { get; set; }
    public string UnidadeFederativaFornecedor { get; set; }
    public string UnidadeFederativaCliente { get; set; }
    public IEnumerable<ItemNotaFiscal> ItensNotaFiscal { get; set; }
    public IEnumerable<ResumoImpostoNotaFiscal> ResumoImpostosNotaFiscal { get; set; }
    public virtual StatusEscrituracao StatusEscrituracao { get; set; }

    public ArquivoNotaFiscalDto ArquivoNotaFiscal { get; set; }

    public class ItemNotaFiscal
    {
        public string Descricao { get; set; }
        public decimal? Valor { get; set; }
        public decimal? BaseCalculoICMS { get; set; }
        public decimal? ICMS { get; set; }
        public decimal? AliquotaICMS { get; set; }
        public decimal? BaseCalculoPISCOFINS { get; set; }
        public decimal? PISCOFINS { get; set; }
        public decimal? AliquotaPISCOFINS { get; set; }
        public decimal? ValorIsencao { get; set; }
    }

    public class ResumoImpostoNotaFiscal
    {
        public string Descricao { get; set; }
        public decimal? BaseCalculo { get; set; }
        public decimal? Aliquota { get; set; }
        public decimal? Valor { get; set; }
    }

    public class ArquivoNotaFiscalDto
    {
        public string Nome { get; set; }
        public string Extensao { get; set; }
        public string UrlGed { get; set; }
    }
}
""" 