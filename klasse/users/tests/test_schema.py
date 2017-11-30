def test_viewer_query(schema, rf, user):
    request = rf.request()
    request.user = user

    query = '''
        query {
            viewer {
                email
            }
        }
    '''

    expected = {'viewer': {'email': 'user@example.com'}}

    result = schema.execute(query, context_value=request)

    assert not result.errors
    assert result.data == expected


def test_viewer_snapshot(schema, rf, user, snapshot):
    request = rf.request()
    request.user = user

    query = '''
        query {
            viewer {
                email
            }
        }
    '''

    result = schema.execute(query, context_value=request)

    snapshot.assert_match(result.data)
