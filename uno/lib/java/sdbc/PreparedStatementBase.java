/*
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020 https://prrvchr.github.io                                     ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
*/
package io.github.prrvchr.uno.sdbc;

import com.sun.star.sdbc.SQLException;

import io.github.prrvchr.uno.helper.UnoHelper;


public abstract class PreparedStatementBase
    extends PreparedStatementMain
{

    // The constructor method:
    // XXX: Constructor called from methods:
    // XXX: - io.github.prrvchr.uno.sdbc.PreparedStatement()
    // XXX: - io.github.prrvchr.uno.sdbc.PreparedStatementSuper()
    public PreparedStatementBase(String service,
                                 String[] services,
                                 ConnectionBase connection,
                                 String sql)
    {
        super(service, services, connection);
        m_Sql = sql;
    }

    @Override
    protected void _createStatement()
        throws SQLException
    {
        checkDisposed();
        if (m_Statement == null) {
            try {
                try {
                    if (m_Sql.startsWith("INSERT ")) {
                        m_Statement = m_Connection.getProvider().getConnection().prepareStatement(m_Sql, m_AutoGeneratedKeys);
                    }
                    else if (m_ResultSetType != java.sql.ResultSet.TYPE_FORWARD_ONLY ||
                        m_ResultSetConcurrency != java.sql.ResultSet.CONCUR_READ_ONLY) {
                        m_Statement = m_Connection.getProvider().getConnection().prepareStatement(m_Sql, m_ResultSetType, m_ResultSetConcurrency);
                    }
                    else {
                        m_Statement = m_Connection.getProvider().getConnection().prepareStatement(m_Sql);
                    }
                    _setStatement();
                } 
                catch (NoSuchMethodError e) {
                    m_Statement = m_Connection.getProvider().getConnection().prepareStatement(m_Sql);
                    System.out.println("sdbc.PreparedStatementBase._createStatement() 2: " + m_ResultSetType + " - " + m_ResultSetConcurrency + " - SQL: '" + m_Sql + "'");
                    _setStatement();
                }
            } 
            catch (java.sql.SQLException e) {
                throw UnoHelper.getSQLException(e, this);
            }
        }
    }


}