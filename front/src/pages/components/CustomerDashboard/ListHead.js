import React from 'react'
import PropTypes from 'prop-types';
// material
import { visuallyHidden } from '@mui/utils';
import { Icon } from '@iconify/react';
import {
  Box,
  TableRow,
  IconButton,
  TableCell,
  TableHead,
  TableSortLabel
} from '@mui/material';
import reloadOutlined from '@iconify/icons-ant-design/reload-outlined';

// ----------------------------------------------------------------------

ListHead.propTypes = {
  order: PropTypes.oneOf(['asc', 'desc']),
  orderBy: PropTypes.string,
  headLabel: PropTypes.array,
  onRequestSort: PropTypes.func,
};

export default function ListHead({
  order,
  orderBy,
  headLabel,
  onRequestSort,
  handleRefresh
}) {
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox" >
          <IconButton onClick={handleRefresh}>
            <Icon icon={reloadOutlined} width={20} height={20} />
          </IconButton>
        </TableCell>
        {headLabel.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.alignRight ? 'right' : 'left'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              hideSortIcon
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box sx={{ ...visuallyHidden }}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}
