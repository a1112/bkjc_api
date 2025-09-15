#include "steelmodeldata.h"

SteelModelData::SteelModelData(QObject *parent)
    : QAbstractItemModel(parent)
{}

QVariant SteelModelData::headerData(int section, Qt::Orientation orientation, int role) const
{
    // FIXME: Implement me!
}

QModelIndex SteelModelData::index(int row, int column, const QModelIndex &parent) const
{
    // FIXME: Implement me!
}

QModelIndex SteelModelData::parent(const QModelIndex &index) const
{
    // FIXME: Implement me!
}

int SteelModelData::rowCount(const QModelIndex &parent) const
{
    if (!parent.isValid())
        return 0;

    // FIXME: Implement me!
}

int SteelModelData::columnCount(const QModelIndex &parent) const
{
    if (!parent.isValid())
        return 0;

    // FIXME: Implement me!
}

QVariant SteelModelData::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return QVariant();

    // FIXME: Implement me!
    return QVariant();
}
