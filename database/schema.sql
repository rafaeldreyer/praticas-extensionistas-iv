-- Controle de Frota - esquema MySQL 8.0+
-- Executar em ambiente de desenvolvimento ou em banco ainda não criado.

CREATE DATABASE IF NOT EXISTS controle_frota
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE controle_frota;

CREATE TABLE usuario (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('ADMINISTRADOR', 'PORTEIRO') NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_usuario_email (email)
) ENGINE=InnoDB;

CREATE TABLE funcionario (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    matricula VARCHAR(30) NOT NULL,
    cpf CHAR(11) NOT NULL,
    numero_cnh VARCHAR(20) NOT NULL,
    categoria_cnh VARCHAR(5) NOT NULL,
    validade_cnh DATE NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_funcionario_matricula (matricula),
    UNIQUE KEY uk_funcionario_cpf (cpf),
    UNIQUE KEY uk_funcionario_numero_cnh (numero_cnh)
) ENGINE=InnoDB;

CREATE TABLE veiculo (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    placa CHAR(7) NOT NULL,
    tipo ENUM('CARRO', 'CAMINHAO', 'MOTO') NOT NULL,
    marca VARCHAR(60) NOT NULL,
    modelo VARCHAR(80) NOT NULL,
    ano_fabricacao SMALLINT UNSIGNED NOT NULL,
    categoria_cnh_minima VARCHAR(5) NOT NULL,
    quilometragem_atual DECIMAL(12,1) UNSIGNED NOT NULL DEFAULT 0,
    status ENUM('DISPONIVEL', 'EM_USO', 'MANUTENCAO', 'INATIVO') NOT NULL DEFAULT 'DISPONIVEL',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_veiculo_placa (placa),
    CONSTRAINT ck_veiculo_ano CHECK (ano_fabricacao BETWEEN 1900 AND 2100)
) ENGINE=InnoDB;

CREATE TABLE saida_veiculo (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    veiculo_id BIGINT UNSIGNED NOT NULL,
    motorista_id BIGINT UNSIGNED NOT NULL,
    registrado_por_id BIGINT UNSIGNED NOT NULL,
    encerrado_por_id BIGINT UNSIGNED NULL,
    data_hora_saida DATETIME NOT NULL,
    quilometragem_saida DECIMAL(12,1) UNSIGNED NOT NULL,
    destino VARCHAR(255) NOT NULL,
    observacao_saida TEXT NULL,
    data_hora_retorno DATETIME NULL,
    quilometragem_retorno DECIMAL(12,1) UNSIGNED NULL,
    observacao_retorno TEXT NULL,
    status ENUM('ABERTA', 'ENCERRADA', 'CANCELADA') NOT NULL DEFAULT 'ABERTA',
    -- Garante no banco que só exista uma saída ABERTA para cada veículo.
    veiculo_em_uso_id BIGINT UNSIGNED GENERATED ALWAYS AS
      (CASE WHEN status = 'ABERTA' THEN veiculo_id ELSE NULL END) STORED,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_saida_motorista_data (motorista_id, data_hora_saida),
    KEY ix_saida_status_data (status, data_hora_saida),
    UNIQUE KEY uk_saida_veiculo_aberta (veiculo_em_uso_id),
    CONSTRAINT fk_saida_veiculo
      FOREIGN KEY (veiculo_id) REFERENCES veiculo (id),
    CONSTRAINT fk_saida_motorista
      FOREIGN KEY (motorista_id) REFERENCES funcionario (id),
    CONSTRAINT fk_saida_registrado_por
      FOREIGN KEY (registrado_por_id) REFERENCES usuario (id),
    CONSTRAINT fk_saida_encerrado_por
      FOREIGN KEY (encerrado_por_id) REFERENCES usuario (id),
    CONSTRAINT ck_saida_retorno_km CHECK
      (quilometragem_retorno IS NULL OR quilometragem_retorno >= quilometragem_saida),
    CONSTRAINT ck_saida_retorno_data CHECK
      (data_hora_retorno IS NULL OR data_hora_retorno >= data_hora_saida),
    CONSTRAINT ck_saida_status_dados CHECK (
      (status = 'ABERTA' AND data_hora_retorno IS NULL AND quilometragem_retorno IS NULL AND encerrado_por_id IS NULL)
      OR (status IN ('ENCERRADA', 'CANCELADA'))
    )
) ENGINE=InnoDB;
