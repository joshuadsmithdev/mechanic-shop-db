from app import create_app
app = create_app({'TESTING': True})
vf = app.view_functions.get('tickets.create_ticket')
print('View func:', vf)
print('Endpoint exists:', 'tickets.create_ticket' in app.view_functions)
print('Module:', getattr(vf, '__module__', None) if vf else None)
doc = (vf.__doc__ or '').strip().splitlines()[0] if (vf and vf.__doc__) else None
print('Doc head:', doc)
