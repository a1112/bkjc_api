# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, SmallInteger, String, Unicode, text
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ComputeNode(Base):
    __tablename__ = 'compute_node'

    id = Column(Integer, primary_key=True)
    name = Column(String(32, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)
    address = Column(String(15, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)
    database = Column(String(30, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False, server_default=text("('master')"))
    instance = Column(String(16, 'Latin1_General_100_CI_AS_KS_WS'), server_default=text("('SQLSERVER')"))
    active = Column(BIT, nullable=False)
    index = Column(Integer, nullable=False)
    driveletter = Column(String(2, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)


class ConfigurationProperties(Base):
    __tablename__ = 'configuration_properties'

    id = Column(String(50, 'Latin1_General_100_CI_AS_KS_WS'), primary_key=True, nullable=False)
    key = Column(String(50, 'Latin1_General_100_CI_AS_KS_WS'), primary_key=True, nullable=False)
    value = Column(Unicode(4000))
    default = Column(Unicode(4000))
    protection = Column(SmallInteger, nullable=False)
    access = Column(SmallInteger, nullable=False)
    datatype = Column(String(50, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)


class DatabaseFile(Base):
    __tablename__ = 'database_file'

    filegroup_id = Column(Integer, primary_key=True, nullable=False)
    sequence = Column(Integer, primary_key=True, nullable=False)
    root_path = Column(Unicode(1000), nullable=False)
    is_add_from_alter = Column(BIT, nullable=False)
    percent_allocated_space = Column(Float(53))


class Distribution(Base):
    __tablename__ = 'distribution'

    id = Column(Integer, primary_key=True)
    name = Column(String(32, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)
    index = Column(Integer, nullable=False)
    numa_port = Column(SmallInteger, nullable=False, server_default=text("((1433))"))


class Filegroup(Base):
    __tablename__ = 'filegroup'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    distribution_id = Column(Integer)
    min_filesize = Column(Unicode(10), nullable=False)
    max_filesize = Column(Unicode(10), nullable=False)
    default_filegrowth = Column(Unicode(10), nullable=False)
    type = Column(Integer, nullable=False)
    is_shell = Column(BIT, nullable=False, server_default=text("((0))"))


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True)
    type = Column(SmallInteger, nullable=False)
    name = Column(String(32, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)
    address = Column(String(15, 'Latin1_General_100_CI_AS_KS_WS'), nullable=False)
    active = Column(BIT, nullable=False)


class PdwSpConfigure(Base):
    __tablename__ = 'pdw_sp_configure'

    name = Column(Unicode(35), primary_key=True)
    minimum = Column(Integer)
    maximum = Column(Integer)
    config_value = Column(Integer)
    run_value = Column(Integer)


class VersionHistory(Base):
    __tablename__ = 'version_history'

    version = Column(Integer, primary_key=True, server_default=text("((0))"))
    date_installed = Column(DateTime, nullable=False)
