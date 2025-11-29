import { Pagination } from "react-bootstrap"

const Pages = () => {
    const PageCount = Math.ceil(10/3)
    const pages = []

    for(let i = 0; i < PageCount; i++) {
        pages.push(i + 1)
    }
    
    const paginationStyle = {
        '--bs-pagination-color': '#dc3545',
        '--bs-pagination-active-bg': '#dc3545',
        '--bs-pagination-active-border-color': '#dc3545'
    }

    return(
        <Pagination style={paginationStyle}>
            {pages.map(page => 
                <Pagination.Item 
                    key={page}
                    style={{ color: 'red !important' }}
                >
                    {page}
                </Pagination.Item>
            )}
        </Pagination>
    )
}

export default Pages