import React from 'react'
import { filter } from 'lodash';
import { Icon } from '@iconify/react';
import { sentenceCase } from 'change-case';
import { useParams } from 'react-router-dom';
import { useConfirm } from 'material-ui-confirm'
import foodIcon from '@iconify/icons-dashicons/food';
import plusCircleOutlined from '@iconify/icons-ant-design/plus-circle-outlined';
import minusCircleOutlined from '@iconify/icons-ant-design/minus-circle-outlined'
import {
  Card,
  IconButton,
  Table,
  Stack,
  Avatar,
  Button,
  TableRow,
  TableBody,
  TableCell,
  Container,
  Typography,
  TableContainer,
  TablePagination
} from '@mui/material';
import Page from '../components/helpers/Page';
import Label from '../components/helpers/Label';
import { getRestaurant, orderSubmit } from 'src/utils/requests';
import Scrollbar from '../components/helpers/Scrollbar';
import SearchNotFound from '../components/helpers/SearchNotFound';
import { RestMenuListHead, RestMenuListToolbar } from './components/restaurantMenu';
import { useAuth } from 'src/utils/useAuth';
import { USER_TYPES } from 'src/utils/values';
import { useNavigate } from 'react-router-dom';


// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'name', label: 'Name', alignRight: false },
  { id: 'count', label: 'Count', alignRight: false },
  { id: 'price', label: 'Price', alignRight: false },
  { id: 'status', label: 'Status', alignRight: false },
  { id: 'total', label: 'Total', alignRight: true },
];

// ----------------------------------------------------------------------

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(array, comparator, query) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query) {
    return filter(array, (_user) => _user.name.toLowerCase().indexOf(query.toLowerCase()) !== -1);
  }
  return stabilizedThis.map((el) => el[0]);
}

export default function RestaurantMenu() {

  const { id } = useParams()
  const [resInfo, setResInfo] = React.useState({})
  const [menu, setMenu] = React.useState([])
  const [totalPrice, setTotalPrice] = React.useState(0)

  const order_inc = (id) => {
    let newMenu = [...menu]
    for (let i = 0; i < newMenu.length; ++i)
      if (newMenu[i].id === id) {
        newMenu[i].count += 1
        setTotalPrice(totalPrice + newMenu[i].price)
        setMenu(newMenu)
        return
      }
  }

  const order_dec = (id) => {
    let newMenu = [...menu]
    for (let i = 0; i < newMenu.length; ++i) {
      if (newMenu[i].id === id && newMenu[i].count > 0) {
        newMenu[i].count -= 1
        setTotalPrice(totalPrice - newMenu[i].price)
        setMenu(newMenu)
        return
      }
    }
  }


  React.useEffect(() => {
    getRestaurant(id)
      .then((res) => {
        setResInfo(res.data)
        setMenu(res.data.menu.map(row => {
          return {
            ...row,
            count: 0,
            statusStr: row?.status ? 'ready' : "not ready",
          }
        }))
      })
      .catch(() => {
        setResInfo({})
        // TODO restauran not found
      })
  }, [])

  const [page, setPage] = React.useState(0);
  const [order, setOrder] = React.useState('asc');
  const [orderBy, setOrderBy] = React.useState('name');
  const [filterName, setFilterName] = React.useState('');
  const [rowsPerPage, setRowsPerPage] = React.useState(5);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleFilterByName = (event) => {
    setFilterName(event.target.value);
  };

  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - menu.length) : 0;

  const filteredMenu = applySortFilter(menu, getComparator(order, orderBy), filterName);

  const confirm = useConfirm()
  const handleOrderClick = () => {
    confirm({
    }).then(() => {
      const orderList = menu.filter(
        (row) => row.count > 0
      ).map((row) => ({
        food_id: row.id,
        quantity: row.count
      })
      )
      orderSubmit(resInfo.id, orderList, authed?.access_token)
        .then(() => {
          navigate('/dashboard', { replace: true });
        })
        .catch(() => {
          // TODO show reason of error
          navigate('/login', { replace: true });
        })
    }).catch(() => { })
  }

  const navigate = useNavigate();
  const handleLinkLogin = () => {
    navigate('/login', { replace: true });
  }

  const { authed } = useAuth()
  const isCustomer = (authed?.object_type + "").toLowerCase() === USER_TYPES.customer

  return (
    <Page title="shabfood">
      <Container>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
          <Typography variant="h4" gutterBottom>
            {resInfo?.name}
          </Typography>
          <Button
            variant="contained"
            startIcon={<Icon icon={foodIcon} />}
            onClick={isCustomer ? handleOrderClick : handleLinkLogin}
            disabled={totalPrice === 0 && isCustomer}
          >
            {isCustomer ?
              ("Order:" + totalPrice) :
              ("need login as customer")}
          </Button>
        </Stack>

        <Card>
          <RestMenuListToolbar
            filterName={filterName}
            onFilterName={handleFilterByName}
          />

          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              <Table>
                <RestMenuListHead
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  onRequestSort={handleRequestSort}
                />
                <TableBody>
                  {filteredMenu
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((row) => {
                      const { id, name, count, price, status, statusStr } = row;

                      return (
                        <TableRow
                          hover
                          key={id}
                          tabIndex={-1}
                          role="checkbox"
                        >
                          <TableCell padding="checkbox">
                            <IconButton onClick={() => order_inc(id)} color='primary' disabled={status === 0}>
                              <Icon icon={plusCircleOutlined} width={20} height={20} />
                            </IconButton>
                            <IconButton onClick={() => order_dec(id)} color='error' disabled={count === 0}>
                              <Icon icon={minusCircleOutlined} width={20} height={20} />
                            </IconButton>
                          </TableCell>
                          <TableCell component="th" scope="row" padding="none">
                            <Stack direction="row" alignItems="center" spacing={2}>
                              <Avatar alt={name} src={"avatarUrl TODO"} />
                              <Typography variant="subtitle2" noWrap>
                                {name}
                              </Typography>
                            </Stack>
                          </TableCell>
                          <TableCell align="left">{count}</TableCell>
                          <TableCell align="left">{price}</TableCell>
                          <TableCell align="left">
                            <Label
                              variant="ghost"
                              color={(status === 0 && 'error') || 'success'}
                            >
                              {sentenceCase(statusStr)}
                            </Label>
                          </TableCell>

                          <TableCell align="right">{count * price}</TableCell>
                        </TableRow>
                      );
                    })}
                  {emptyRows > 0 && (
                    <TableRow style={{ height: 53 * emptyRows }}>
                      <TableCell colSpan={6} />
                    </TableRow>
                  )}
                </TableBody>
                {(filteredMenu.length === 0) && (
                  <TableBody>
                    <TableRow>
                      <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                        <SearchNotFound searchQuery={filterName} />
                      </TableCell>
                    </TableRow>
                  </TableBody>
                )}
              </Table>
            </TableContainer>
          </Scrollbar>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={menu.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Card>
      </Container>
    </Page>
  );
}
